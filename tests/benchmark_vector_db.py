
import time
import numpy as np
import sys
import os

# Add repo root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from memory.lightweight_vector_db import HNSWIndex, LightweightVectorDB

def benchmark_search():
    print("🚀 Benchmarking HNSWIndex search...")

    # Setup
    index = HNSWIndex(dimension=384)
    num_vectors = 2000

    # Generate random vectors
    print(f"Generating {num_vectors} vectors...")
    np.random.seed(42)
    vectors = np.random.randn(num_vectors, 384).astype(np.float32)
    # Normalize vectors
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    vectors = vectors / norms

    # Add to index
    for i in range(num_vectors):
        index.add(i, vectors[i])

    # Query vector
    query = np.random.randn(384).astype(np.float32)
    query = query / np.linalg.norm(query)

    # Benchmark
    print("Running search...")
    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        index.search(query, k=5)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations * 1000
    print(f"Average search time: {avg_time:.4f} ms per query")
    return avg_time

if __name__ == "__main__":
    benchmark_search()
