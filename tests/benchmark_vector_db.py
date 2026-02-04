
import time
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.lightweight_vector_db import HNSWIndex

def benchmark():
    dimension = 384
    num_vectors = 2000 # Enough to show difference, but quick to run

    print(f"Generating {num_vectors} random vectors of dimension {dimension}...")

    index = HNSWIndex(dimension=dimension)

    # Generate random vectors
    np.random.seed(42)
    vectors = np.random.randn(num_vectors, dimension).astype(np.float32)

    # Normalize them to simulate real embeddings
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    vectors = vectors / norms

    start_time = time.time()
    for i in range(num_vectors):
        index.add(i, vectors[i])
    print(f"Adding vectors took: {time.time() - start_time:.4f}s")

    # Generate query vector
    query = np.random.randn(dimension).astype(np.float32)
    query = query / np.linalg.norm(query)

    print("Benchmarking search...")
    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        index.search(query, k=5)

    total_time = time.time() - start_time
    avg_time = total_time / iterations

    print(f"Total time for {iterations} searches: {total_time:.4f}s")
    print(f"Average time per search: {avg_time:.6f}s")

if __name__ == "__main__":
    benchmark()
