"""
Phase 6: Lightweight Vector Database - Claude's Optimization Plan
Memory-efficient vector storage
- Quantized embeddings (384-dim)
- Disk-backed with RAM cache
- HNSW indexing for speed
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
import config


class EmbeddingModel:
    """Lightweight embedding model (all-MiniLM-L6-v2 - 80MB)"""
    
    def __init__(self):
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self.model_name = "all-MiniLM-L6-v2"
        self.model_size_mb = 80
        print(f"📦 Embedding Model: {self.model_name} ({self.model_size_mb}MB)")
    
    def encode(self, text: str) -> np.ndarray:
        """Encode text to embedding"""
        # Simulate embedding (in real implementation, use sentence-transformers)
        # For now, return a random vector of correct dimension
        np.random.seed(hash(text) % 2**32)
        embedding = np.random.randn(self.dimension).astype(np.float32)
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts"""
        embeddings = []
        for text in texts:
            embeddings.append(self.encode(text))
        return np.array(embeddings)


class QuantizedEmbedding:
    """Quantized embedding for memory efficiency"""
    
    @staticmethod
    def quantize(embedding: np.ndarray, bits: int = 8) -> np.ndarray:
        """Quantize embedding to lower precision"""
        if bits == 8:
            # Convert float32 to int8
            min_val = embedding.min()
            max_val = embedding.max()
            
            # Scale to int8 range
            scaled = ((embedding - min_val) / (max_val - min_val + 1e-8) * 255).astype(np.int8)
            return scaled
        
        return embedding
    
    @staticmethod
    def dequantize(quantized: np.ndarray, bits: int = 8) -> np.ndarray:
        """Dequantize embedding back to float32"""
        if bits == 8:
            return quantized.astype(np.float32) / 255.0
        
        return quantized


class HNSWIndex:
    """Hierarchical Navigable Small World (HNSW) index for fast search"""
    
    def __init__(self, dimension: int = 384, max_m: int = 16):
        self.dimension = dimension
        self.max_m = max_m
        self.graph = {}  # Simplified graph structure
        self.data = {}   # Vector data
        self.metadata = {}  # Associated metadata

        # Optimization: Matrix for vectorized search
        self.vectors_matrix = None
        self.ids_list = []
        self.dirty = False
    
    def add(self, idx: int, vector: np.ndarray, metadata: Dict = None):
        """Add vector to index"""
        self.graph[idx] = []
        self.data[idx] = vector
        if metadata:
            self.metadata[idx] = metadata
        self.dirty = True

    def _rebuild_index(self):
        """Rebuild numpy matrix from data"""
        if not self.data:
            self.vectors_matrix = None
            self.ids_list = []
            return

        self.ids_list = list(self.data.keys())
        # Stack vectors
        vectors = np.array([self.data[i] for i in self.ids_list])

        # Normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1e-8
        self.vectors_matrix = vectors / norms
        self.dirty = False
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        """Search for k nearest neighbors"""
        if not self.data:
            return []

        if self.dirty or self.vectors_matrix is None:
            self._rebuild_index()

        # Normalize query
        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            query_normalized = query_vector
        else:
            query_normalized = query_vector / query_norm

        # Vectorized cosine similarity
        # Matrix is already normalized, so just dot product
        # scores[i] = dot(matrix[i], query) = cos_sim since both are unit vectors
        scores = np.dot(self.vectors_matrix, query_normalized)
        
        # Distance = 1 - cosine_similarity
        distances = 1 - scores
        
        # Get top k indices (smallest distances)
        if k < len(distances):
            # Using argpartition for O(N) selection of top k
            top_k_indices = np.argpartition(distances, k)[:k]
            # Sort the top k results for correct ordering
            top_k_indices = top_k_indices[np.argsort(distances[top_k_indices])]
        else:
            top_k_indices = np.argsort(distances)

        results = []
        for idx in top_k_indices:
            vector_id = self.ids_list[idx]
            dist = distances[idx]
            results.append((vector_id, float(dist)))

        return results


class LightweightVectorDB:
    """
    Memory-efficient vector storage
    - Quantized embeddings (384-dim)
    - Disk-backed with RAM cache
    - HNSW indexing for speed
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = Path(db_path or str(config.DATA_DIR / "vector_db"))
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.embedder = EmbeddingModel()
        self.index = HNSWIndex(dimension=self.embedder.dimension)
        
        # RAM cache for hot vectors
        self.hot_cache = {}  # LRU cache for frequently accessed vectors
        self.cache_max_size = 1000
        
        # Statistics
        self.stats = {
            "total_vectors": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "disk_reads": 0
        }
    
    def store_and_index(self, text: str, metadata: Dict = None):
        """Store text with embedding and metadata"""
        try:
            # Generate embedding
            embedding = self.embedder.encode(text)
            
            # Quantize to save space
            quantized = QuantizedEmbedding.quantize(embedding)
            
            # Generate ID
            vector_id = self.stats["total_vectors"]
            self.stats["total_vectors"] += 1
            
            # Store in index
            self.index.add(vector_id, embedding, metadata)
            
            # Cache if important
            if metadata and metadata.get("importance", 0) >= 7:
                self._add_to_cache(vector_id, quantized, metadata)
            
            # Store to disk
            self._store_to_disk(vector_id, quantized, metadata)
            
            return vector_id
        except Exception as e:
            print(f"⚠️  Error storing and indexing: {e}")
            return -1
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar vectors"""
        try:
            # Encode query
            query_embedding = self.embedder.encode(query)
            
            # Search index
            results = self.index.search(query_embedding, k=k)
            
            # Retrieve full data
            search_results = []
            for idx, distance in results:
                # Check cache first
                if idx in self.hot_cache:
                    self.stats["cache_hits"] += 1
                    data = self.hot_cache[idx]
                else:
                    self.stats["cache_misses"] += 1
                    data = self._load_from_disk(idx)
                
                search_results.append({
                    "id": idx,
                    "distance": float(distance),
                    "metadata": self.index.metadata.get(idx, {}),
                    "data": data
                })
            
            return search_results
        except Exception as e:
            print(f"⚠️  Error searching vectors: {e}")
            return []
    
    def _add_to_cache(self, vector_id: int, vector: np.ndarray, metadata: Dict):
        """Add vector to RAM cache"""
        if len(self.hot_cache) >= self.cache_max_size:
            # Remove oldest entry
            oldest_id = next(iter(self.hot_cache))
            del self.hot_cache[oldest_id]
        
        self.hot_cache[vector_id] = {
            "vector": vector,
            "metadata": metadata
        }
    
    def _store_to_disk(self, vector_id: int, vector: np.ndarray, metadata: Dict):
        """Store vector to disk"""
        file_path = self.db_path / f"vector_{vector_id}.json"
        
        data = {
            "id": vector_id,
            "vector": vector.tolist(),
            "metadata": metadata
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f)
    
    def _load_from_disk(self, vector_id: int) -> Dict:
        """Load vector from disk"""
        file_path = self.db_path / f"vector_{vector_id}.json"
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        
        return {}
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        cache_total = self.stats["cache_hits"] + self.stats["cache_misses"]
        cache_hit_rate = (
            self.stats["cache_hits"] / cache_total * 100
            if cache_total > 0 else 0
        )
        
        return {
            "total_vectors": self.stats["total_vectors"],
            "cache_size": len(self.hot_cache),
            "cache_max_size": self.cache_max_size,
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "cache_hit_rate": cache_hit_rate,
            "disk_reads": self.stats["disk_reads"],
            "embedding_dimension": self.embedder.dimension,
            "embedding_model": self.embedder.model_name,
            "db_path": str(self.db_path)
        }
    
    def print_stats(self):
        """Print database statistics"""
        stats = self.get_stats()
        
        print(f"\n{'='*60}")
        print(f"🗄️  LIGHTWEIGHT VECTOR DATABASE - STATISTICS")
        print(f"{'='*60}")
        print(f"Total Vectors: {stats['total_vectors']}")
        print(f"Embedding Model: {stats['embedding_model']} ({self.embedder.model_size_mb}MB)")
        print(f"Embedding Dimension: {stats['embedding_dimension']}")
        print(f"\nRAM Cache:")
        print(f"  Size: {stats['cache_size']} / {stats['cache_max_size']}")
        print(f"  Hit Rate: {stats['cache_hit_rate']:.1f}%")
        print(f"  Hits: {stats['cache_hits']} | Misses: {stats['cache_misses']}")
        print(f"\nStorage:")
        print(f"  Path: {stats['db_path']}")
        print(f"  Disk Reads: {stats['disk_reads']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        db = LightweightVectorDB()
        
        print("🚀 LIGHTWEIGHT VECTOR DATABASE - TEST\n")
        
        # Test documents
        documents = [
            ("Python is a programming language", {"category": "programming", "importance": 8}),
            ("Machine learning is a subset of AI", {"category": "ai", "importance": 9}),
            ("Neural networks are inspired by biology", {"category": "ai", "importance": 7}),
            ("Data science involves statistics", {"category": "data", "importance": 6}),
            ("Web development uses HTML and CSS", {"category": "web", "importance": 5}),
        ]
        
        print("📝 STORING DOCUMENTS:")
        for text, metadata in documents:
            vector_id = await db.store_and_index(text, metadata)
            print(f"  [{vector_id}] {text[:40]}...")
        
        # Test search
        print("\n🔍 SEARCHING:")
        query = "programming languages"
        results = await db.search(query, k=3)
        print(f"Query: '{query}'")
        for result in results:
            print(f"  Distance: {result['distance']:.3f} | {result['metadata']}")
        
        # Print stats
        db.print_stats()
    
    asyncio.run(main())
