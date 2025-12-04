"""
Phase 4: Tiered Memory System - Claude's Optimization Plan
3-Tier Memory Architecture:
- Tier 1: VRAM (6GB) - Active inference
- Tier 2: RAM (24GB) - Hot cache
- Tier 3: SSD (512GB) - Long-term storage
"""

import json
import sqlite3
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import config


class VRAMCache:
    """Tier 1: VRAM Cache (6GB) - Active inference data"""
    
    def __init__(self, max_size_gb: float = 6.0):
        self.max_size_gb = max_size_gb
        self.cache = {}
        self.size_used = 0.0
        self.access_count = {}
    
    def store(self, key: str, value: Any, size_mb: float = 1.0):
        """Store data in VRAM cache"""
        if self.size_used + size_mb > self.max_size_gb * 1024:
            # Evict least recently used
            self._evict_lru()
        
        self.cache[key] = value
        self.size_used += size_mb
        self.access_count[key] = 0
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from VRAM cache"""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if not self.cache:
            return
        
        lru_key = min(self.access_count, key=self.access_count.get)
        del self.cache[lru_key]
        del self.access_count[lru_key]
        self.size_used -= 1.0  # Approximate


class RAMCache:
    """Tier 2: RAM Cache (24GB) - Hot cache for frequently accessed data"""
    
    def __init__(self, max_size_gb: float = 20.0):
        self.max_size_gb = max_size_gb
        self.cache = {}
        self.size_used = 0.0
        self.access_count = {}
        self.last_access = {}
    
    def store(self, key: str, value: Any, size_mb: float = 1.0):
        """Store data in RAM cache"""
        if self.size_used + size_mb > self.max_size_gb * 1024:
            self._evict_lru()
        
        self.cache[key] = value
        self.size_used += size_mb
        self.access_count[key] = 0
        self.last_access[key] = datetime.now()
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from RAM cache"""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            self.last_access[key] = datetime.now()
            return self.cache[key]
        return None
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search cache for matching items"""
        results = []
        for key, value in list(self.cache.items())[:limit]:
            if query.lower() in str(value).lower():
                results.append({
                    "key": key,
                    "value": value,
                    "access_count": self.access_count.get(key, 0)
                })
        return results
    
    def promote(self, key: str):
        """Promote item to higher priority"""
        if key in self.access_count:
            self.access_count[key] += 10  # Boost priority
    
    def _evict_lru(self):
        """Evict least recently used item"""
        if not self.cache:
            return
        
        lru_key = min(self.access_count, key=self.access_count.get)
        del self.cache[lru_key]
        del self.access_count[lru_key]
        del self.last_access[lru_key]
        self.size_used -= 1.0


class SSDStore:
    """Tier 3: SSD Store (512GB) - Long-term storage"""
    
    def __init__(self, path: str = "C:/Ananta_Cache", max_size_gb: float = 50.0):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.max_size_gb = max_size_gb
        self.db_path = self.path / "ananta_memory.db"
        self.hot_cache_path = self.path / "hot_cache"
        self.cold_cache_path = self.path / "cold_cache"
        
        self.hot_cache_path.mkdir(exist_ok=True)
        self.cold_cache_path.mkdir(exist_ok=True)
        
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT,
                importance REAL,
                access_count INTEGER,
                created_at TIMESTAMP,
                last_accessed TIMESTAMP,
                storage_type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_hot(self, data: Dict):
        """Store frequently accessed data on hot SSD cache"""
        try:
            data_id = data.get("id", str(datetime.now().timestamp()))
            
            # Store in hot cache
            hot_file = self.hot_cache_path / f"{data_id}.json"
            with open(hot_file, 'w') as f:
                json.dump(data, f)
            
            # Record in database
            self._record_in_db(data_id, data, "hot")
        except Exception as e:
            print(f"⚠️  Error storing hot data: {e}")
    
    def store_cold(self, data: Dict):
        """Store infrequently accessed data on cold SSD cache (compressed)"""
        try:
            data_id = data.get("id", str(datetime.now().timestamp()))
            
            # Store in cold cache
            cold_file = self.cold_cache_path / f"{data_id}.json"
            with open(cold_file, 'w') as f:
                json.dump(data, f)
            
            # Record in database
            self._record_in_db(data_id, data, "cold")
        except Exception as e:
            print(f"⚠️  Error storing cold data: {e}")
    
    def search_hot(self, query: str, limit: int = 5) -> List[Dict]:
        """Search hot cache for matching items"""
        results = []
        
        try:
            if not self.hot_cache_path.exists():
                return results
            
            for file in list(self.hot_cache_path.glob("*.json"))[:limit]:
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        if query.lower() in json.dumps(data).lower():
                            results.append(data)
                except Exception as e:
                    print(f"⚠️  Error reading file {file}: {e}")
        except Exception as e:
            print(f"⚠️  Error searching hot cache: {e}")
        
        return results
    
    def _record_in_db(self, data_id: str, data: Dict, storage_type: str):
        """Record data in database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, importance, access_count, created_at, last_accessed, storage_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data_id,
            json.dumps(data),
            data.get("importance", 5.0),
            0,
            datetime.now(),
            datetime.now(),
            storage_type
        ))
        
        conn.commit()
        conn.close()


class TieredMemorySystem:
    """
    3-Tier Memory Architecture:
    - Tier 1: VRAM (6GB) - Active inference
    - Tier 2: RAM (24GB) - Hot cache
    - Tier 3: SSD (512GB) - Long-term storage
    """
    
    def __init__(self):
        self.vram_cache = VRAMCache(max_size_gb=6)
        self.ram_cache = RAMCache(max_size_gb=20)
        self.ssd_store = SSDStore(path=str(config.DATA_DIR / "tiered_memory"))
    
    def store_conversation(self, conversation: Dict):
        """Intelligent storage routing based on importance"""
        try:
            importance = self.calculate_importance(conversation)
            
            if importance >= 8:
                # Critical - keep in RAM for fast access
                self.ram_cache.store(
                    conversation.get("id", str(datetime.now())),
                    conversation,
                    size_mb=1.0
                )
                print(f"  📌 Stored in RAM (importance: {importance})")
            
            elif importance >= 5:
                # Important - fast SSD access
                self.ssd_store.store_hot(conversation)
                print(f"  💾 Stored in hot SSD (importance: {importance})")
            
            else:
                # Archive - compress and store
                compressed = self.compress(conversation)
                self.ssd_store.store_cold(compressed)
                print(f"  📦 Stored in cold SSD (importance: {importance})")
        except Exception as e:
            print(f"⚠️  Error storing conversation: {e}")
    
    def retrieve_context(self, query: str, max_results: int = 5) -> List[Dict]:
        """Fast context retrieval from all tiers"""
        results = []
        
        try:
            # Check RAM first (fastest)
            ram_results = self.ram_cache.search(query, limit=max_results)
            results.extend(ram_results)
            
            if len(results) >= max_results:
                return results[:max_results]
            
            # Check hot SSD cache
            ssd_hot = self.ssd_store.search_hot(
                query,
                limit=max_results - len(results)
            )
            results.extend(ssd_hot)
            
            # Promote frequently accessed to RAM
            for result in results:
                if result.get("access_count", 0) > 5:
                    self.ram_cache.promote(result.get("key", ""))
        except Exception as e:
            print(f"⚠️  Error retrieving context: {e}")
        
        return results[:max_results]
    
    def calculate_importance(self, conversation: Dict) -> float:
        """Calculate conversation importance (0-10 scale)"""
        score = 0.0
        
        # Recent conversations are important
        if conversation.get("recency", 0) > 0.8:
            score += 3.0
        
        # Frequently accessed are important
        if conversation.get("access_count", 0) > 10:
            score += 3.0
        
        # User-marked important
        if conversation.get("marked_important", False):
            score += 2.0
        
        # Contains code or technical content
        if any(kw in str(conversation).lower() for kw in ["code", "error", "bug", "fix"]):
            score += 1.5
        
        return min(score, 10.0)
    
    def compress(self, data: Dict) -> Dict:
        """Compress data for storage"""
        compressed = {
            "id": data.get("id"),
            "summary": str(data)[:500],  # Keep first 500 chars
            "importance": data.get("importance", 5.0),
            "timestamp": datetime.now().isoformat()
        }
        return compressed
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "vram_used_mb": self.vram_cache.size_used,
            "vram_max_mb": self.vram_cache.max_size_gb * 1024,
            "ram_used_mb": self.ram_cache.size_used,
            "ram_max_mb": self.ram_cache.max_size_gb * 1024,
            "vram_items": len(self.vram_cache.cache),
            "ram_items": len(self.ram_cache.cache),
            "ssd_path": str(self.ssd_store.path)
        }
    
    def print_memory_info(self):
        """Print memory information"""
        stats = self.get_memory_stats()
        
        print(f"\n{'='*60}")
        print(f"💾 TIERED MEMORY SYSTEM - STATISTICS")
        print(f"{'='*60}")
        print(f"VRAM Cache:")
        print(f"  Used: {stats['vram_used_mb']:.1f}MB / {stats['vram_max_mb']:.1f}MB")
        print(f"  Items: {stats['vram_items']}")
        print(f"\nRAM Cache:")
        print(f"  Used: {stats['ram_used_mb']:.1f}MB / {stats['ram_max_mb']:.1f}MB")
        print(f"  Items: {stats['ram_items']}")
        print(f"\nSSD Store:")
        print(f"  Path: {stats['ssd_path']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        system = TieredMemorySystem()
        
        print("🚀 TIERED MEMORY SYSTEM - TEST\n")
        
        # Test storing conversations
        conversations = [
            {
                "id": "conv_1",
                "content": "Important conversation about architecture",
                "importance": 9.0,
                "recency": 0.9,
                "access_count": 15
            },
            {
                "id": "conv_2",
                "content": "Regular chat about weather",
                "importance": 3.0,
                "recency": 0.2,
                "access_count": 1
            },
            {
                "id": "conv_3",
                "content": "Code debugging session with error fixes",
                "importance": 7.5,
                "recency": 0.7,
                "access_count": 8
            }
        ]
        
        print("📝 STORING CONVERSATIONS:")
        for conv in conversations:
            await system.store_conversation(conv)
        
        # Print stats
        system.print_memory_info()
        
        # Test retrieval
        print("🔍 RETRIEVING CONTEXT:")
        results = await system.retrieve_context("architecture", max_results=2)
        print(f"Found {len(results)} results")
    
    asyncio.run(main())
