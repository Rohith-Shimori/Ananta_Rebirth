# adaptive_memory.py - Adaptive Memory System with Importance Levels
"""
Structured memory using SQLite with importance levels.
Replaces simple JSON lists with scalable, queryable storage.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid
import threading

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MEMORY_DB = os.path.join(DATA_DIR, "adaptive_memory.db")

class AdaptiveMemory:
    """
    Advanced memory system with:
    - Importance levels (1-10)
    - Decay over time
    - Structured queries
    - Relationship tracking

    Optimized with persistent connection and WAL mode.
    """
    
    def __init__(self, db_path: str = None):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.db_path = db_path or MEMORY_DB
        
        # Thread safety for persistent connection
        self.lock = threading.RLock()
        
        # Persistent connection
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Optional: allows accessing columns by name, but keeping default for now to minimize changes
        
        # Enable WAL mode for performance
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        
        self._init_database()

    def __del__(self):
        """Ensure connection is closed on deletion."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def _init_database(self):
        """Initialize database schema."""
        with self.lock:
            cursor = self.conn.cursor()

            # Main memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    importance INTEGER DEFAULT 5,
                    timestamp REAL NOT NULL,
                    last_accessed REAL,
                    access_count INTEGER DEFAULT 0,
                    decay_factor REAL DEFAULT 1.0,
                    tags TEXT,
                    metadata TEXT
                )
            """)

            # Facts table (structured personal data)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    value TEXT NOT NULL,
                    importance INTEGER DEFAULT 7,
                    confidence REAL DEFAULT 1.0,
                    source TEXT,
                    timestamp REAL NOT NULL,
                    last_updated REAL
                )
            """)

            # Relationships table (connections between memories)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    id TEXT PRIMARY KEY,
                    memory_id_1 TEXT NOT NULL,
                    memory_id_2 TEXT NOT NULL,
                    relationship_type TEXT,
                    strength REAL DEFAULT 0.5,
                    FOREIGN KEY (memory_id_1) REFERENCES memories(id),
                    FOREIGN KEY (memory_id_2) REFERENCES memories(id)
                )
            """)

            # Indices for fast queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON memories(memory_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category)")

            self.conn.commit()
    
    def add_memory(self, role: str, content: str, memory_type: str = "conversation",
                   importance: int = 5, tags: List[str] = None, metadata: Dict = None) -> str:
        """
        Add a new memory with importance level.
        
        Args:
            role: 'user' or 'assistant'
            content: The actual message
            memory_type: 'conversation', 'fact', 'insight', 'task'
            importance: 1-10, higher = more important
            tags: List of tags for categorization
            metadata: Additional structured data
        
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().timestamp()
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO memories (id, role, content, memory_type, importance,
                                     timestamp, last_accessed, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_id,
                role,
                content,
                memory_type,
                min(10, max(1, importance)),  # Clamp 1-10
                timestamp,
                timestamp,
                json.dumps(tags or []),
                json.dumps(metadata or {})
            ))
            self.conn.commit()
        
        return memory_id
    
    def get_important_memories(self, min_importance: int = 7, limit: int = 10) -> List[Dict]:
        """
        Retrieve memories above a certain importance threshold.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, role, content, memory_type, importance, timestamp,
                       access_count, tags, metadata
                FROM memories
                WHERE importance >= ? AND decay_factor > 0.3
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
            """, (min_importance, limit))

            rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            memories.append({
                "id": row[0],
                "role": row[1],
                "content": row[2],
                "type": row[3],
                "importance": row[4],
                "timestamp": row[5],
                "access_count": row[6],
                "tags": json.loads(row[7]) if row[7] else [],
                "metadata": json.loads(row[8]) if row[8] else {}
            })
        
        return memories
    
    def get_recent_memories(self, limit: int = 10, memory_type: Optional[str] = None) -> List[Dict]:
        """
        Get recent memories, optionally filtered by type.
        """
        with self.lock:
            cursor = self.conn.cursor()

            if memory_type:
                cursor.execute("""
                    SELECT id, role, content, memory_type, importance, timestamp
                    FROM memories
                    WHERE memory_type = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (memory_type, limit))
            else:
                cursor.execute("""
                    SELECT id, role, content, memory_type, importance, timestamp
                    FROM memories
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))

            rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            memories.append({
                "id": row[0],
                "role": row[1],
                "content": row[2],
                "type": row[3],
                "importance": row[4],
                "timestamp": row[5]
            })
        
        return memories
    
    def update_importance(self, memory_id: str, new_importance: int):
        """Update the importance level of a memory."""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE memories
                SET importance = ?
                WHERE id = ?
            """, (min(10, max(1, new_importance)), memory_id))
            self.conn.commit()
    
    def access_memory(self, memory_id: str):
        """
        Mark a memory as accessed (updates last_accessed and access_count).
        Frequently accessed memories maintain higher importance.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE memories
                SET last_accessed = ?,
                    access_count = access_count + 1
                WHERE id = ?
            """, (datetime.now().timestamp(), memory_id))
            self.conn.commit()
    
    def decay_memories(self, decay_rate: float = 0.95):
        """
        Apply time-based decay to all memories.
        Reduces importance of old, unaccessed memories.
        Should be called periodically (e.g., daily).
        """
        with self.lock:
            cursor = self.conn.cursor()
            # Decay factor reduces over time, but frequently accessed memories decay slower
            cursor.execute("""
                UPDATE memories
                SET decay_factor = decay_factor * ?
                WHERE access_count < 3
            """, (decay_rate,))
            self.conn.commit()
    
    def store_fact(self, category: str, value: str, importance: int = 7, 
                   confidence: float = 1.0, source: str = "user") -> str:
        """
        Store a structured fact with importance.
        """
        fact_id = str(uuid.uuid4())
        timestamp = datetime.now().timestamp()
        
        with self.lock:
            cursor = self.conn.cursor()

            # Check if fact already exists, update if so
            cursor.execute("SELECT id FROM facts WHERE category = ?", (category,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE facts
                    SET value = ?, importance = ?, confidence = ?,
                        last_updated = ?, source = ?
                    WHERE category = ?
                """, (value, importance, confidence, timestamp, source, category))
                fact_id = existing[0]
            else:
                cursor.execute("""
                    INSERT INTO facts (id, category, value, importance, confidence,
                                      source, timestamp, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (fact_id, category, value, importance, confidence, source, timestamp, timestamp))

            self.conn.commit()
        
        return fact_id
    
    def get_fact(self, category: str) -> Optional[Dict]:
        """Retrieve a fact by category."""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, category, value, importance, confidence, source, timestamp
                FROM facts
                WHERE category = ?
            """, (category,))

            row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "category": row[1],
                "value": row[2],
                "importance": row[3],
                "confidence": row[4],
                "source": row[5],
                "timestamp": row[6]
            }
        return None
    
    def get_all_facts(self, min_importance: int = 1) -> List[Dict]:
        """Get all facts above a certain importance."""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT category, value, importance, confidence
                FROM facts
                WHERE importance >= ?
                ORDER BY importance DESC, timestamp DESC
            """, (min_importance,))

            rows = cursor.fetchall()
        
        facts = []
        for row in rows:
            facts.append({
                "category": row[0],
                "value": row[1],
                "importance": row[2],
                "confidence": row[3]
            })
        
        return facts
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Simple text search in memories.
        (For better semantic search, use with embeddings separately)
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, role, content, memory_type, importance, timestamp
                FROM memories
                WHERE content LIKE ?
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
            """, (f"%{query}%", limit))

            rows = cursor.fetchall()
        
        memories = []
        for row in rows:
            memories.append({
                "id": row[0],
                "role": row[1],
                "content": row[2],
                "type": row[3],
                "importance": row[4],
                "timestamp": row[5]
            })
        
        return memories
    
    def create_relationship(self, memory_id_1: str, memory_id_2: str, 
                           relationship_type: str = "related", strength: float = 0.5) -> str:
        """
        Create a relationship between two memories.
        Useful for building knowledge graphs.
        """
        rel_id = str(uuid.uuid4())
        
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO relationships (id, memory_id_1, memory_id_2, relationship_type, strength)
                VALUES (?, ?, ?, ?, ?)
            """, (rel_id, memory_id_1, memory_id_2, relationship_type, strength))
            self.conn.commit()
        
        return rel_id
    
    def get_related_memories(self, memory_id: str) -> List[Dict]:
        """Get all memories related to a given memory."""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.id, m.content, m.importance, r.relationship_type, r.strength
                FROM memories m
                JOIN relationships r ON (m.id = r.memory_id_2)
                WHERE r.memory_id_1 = ?
                ORDER BY r.strength DESC
            """, (memory_id,))

            rows = cursor.fetchall()
        
        related = []
        for row in rows:
            related.append({
                "id": row[0],
                "content": row[1],
                "importance": row[2],
                "relationship": row[3],
                "strength": row[4]
            })
        
        return related
    
    def get_statistics(self) -> Dict:
        """Get memory system statistics."""
        with self.lock:
            cursor = self.conn.cursor()

            # Count memories by type
            cursor.execute("SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type")
            type_counts = dict(cursor.fetchall())

            # Count facts
            cursor.execute("SELECT COUNT(*) FROM facts")
            fact_count_row = cursor.fetchone()
            fact_count = fact_count_row[0] if fact_count_row else 0

            # Average importance
            cursor.execute("SELECT AVG(importance) FROM memories")
            avg_row = cursor.fetchone()
            avg_importance = avg_row[0] if avg_row and avg_row[0] else 0

            # High importance count
            cursor.execute("SELECT COUNT(*) FROM memories WHERE importance >= 8")
            crit_row = cursor.fetchone()
            critical_count = crit_row[0] if crit_row else 0
        
        return {
            "total_memories": sum(type_counts.values()),
            "memories_by_type": type_counts,
            "total_facts": fact_count,
            "average_importance": round(avg_importance, 2),
            "critical_memories": critical_count
        }
    
    def clear_low_importance(self, threshold: int = 3):
        """Remove memories below importance threshold (cleanup)."""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM memories
                WHERE importance < ? AND decay_factor < 0.5
            """, (threshold,))
            deleted = cursor.rowcount
            self.conn.commit()
        
        return deleted

    def clear_personal(self) -> Dict:
        """Clear personal facts and any personal-type memories."""
        with self.lock:
            cursor = self.conn.cursor()

            # Clear structured facts
            cursor.execute("DELETE FROM facts")
            facts_deleted = cursor.rowcount

            # Clear memories explicitly marked as personal
            cursor.execute(
                "DELETE FROM memories WHERE memory_type = ?",
                ("personal",),
            )
            memories_deleted = cursor.rowcount

            self.conn.commit()

        return {
            "cleared_facts": facts_deleted if facts_deleted is not None else 0,
            "cleared_personal_memories": memories_deleted if memories_deleted is not None else 0,
        }

    def clear_conversation(self) -> int:
        """Clear conversation-type memories (chat history)."""
        with self.lock:
            cursor = self.conn.cursor()

            cursor.execute(
                "DELETE FROM memories WHERE memory_type = ?",
                ("conversation",),
            )
            deleted = cursor.rowcount or 0

            self.conn.commit()

        return deleted
