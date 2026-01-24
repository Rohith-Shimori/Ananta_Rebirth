
import time
import numpy as np
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.lightweight_vector_db import HNSWIndex, EmbeddingModel

def benchmark_search():
    print("🚀 Benchmarking HNSWIndex Search...")

    # Initialize index
    dimension = 384
    index = HNSWIndex(dimension=dimension)

    # Create fake data
    num_vectors = 10000
    print(f"Generating {num_vectors} random vectors of dimension {dimension}...")

    # Pre-generate random normalized vectors
    vectors = np.random.randn(num_vectors, dimension).astype(np.float32)
    vectors /= np.linalg.norm(vectors, axis=1)[:, np.newaxis]

    # Add to index
    start_add = time.time()
    for i in range(num_vectors):
        index.add(i, vectors[i])
    print(f"Adding took: {time.time() - start_add:.4f}s")

    # Benchmark search
    num_queries = 100
    query_vectors = np.random.randn(num_queries, dimension).astype(np.float32)
    query_vectors /= np.linalg.norm(query_vectors, axis=1)[:, np.newaxis]

    print(f"Running {num_queries} searches...")
    start_search = time.time()

    for i in range(num_queries):
        index.search(query_vectors[i], k=5)

    total_time = time.time() - start_search
    avg_time = total_time / num_queries

    print(f"Total search time: {total_time:.4f}s")
    print(f"Average time per search: {avg_time:.4f}s")

    return avg_time

if __name__ == "__main__":
    benchmark_search()
