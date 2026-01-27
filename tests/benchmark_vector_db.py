import time
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.lightweight_vector_db import HNSWIndex

def benchmark():
    print("Initializing HNSWIndex...")
    D = 384
    index = HNSWIndex(dimension=D)
    N = 10000

    print(f"Generating {N} vectors of dimension {D}...")
    np.random.seed(42)
    vectors = np.random.randn(N, D).astype(np.float32)
    # Normalize vectors
    vectors /= np.linalg.norm(vectors, axis=1)[:, np.newaxis]

    print("Populating index...")
    for i in range(N):
        index.add(i, vectors[i])

    query = np.random.randn(D).astype(np.float32)
    query /= np.linalg.norm(query)

    print("Benchmarking search...")
    start_time = time.perf_counter()
    k = 5
    # Run multiple times to get average
    iterations = 5
    for _ in range(iterations):
        results = index.search(query, k=k)
    end_time = time.perf_counter()

    avg_duration = (end_time - start_time) / iterations
    print(f"Average search time for {N} vectors: {avg_duration:.6f} seconds")

    # Correctness check
    print("Verifying correctness...")
    # Brute force
    dots = np.dot(vectors, query)
    best_idx = np.argmax(dots)
    # Note: The implementation uses 1 - dot / (norm*norm)
    # Since we normalized, norm=1. So distance = 1 - dot.
    best_dist = 1 - dots[best_idx]

    top_result = results[0]
    print(f"Top result: ID={top_result[0]}, Dist={top_result[1]:.6f}")
    print(f"Expected:   ID={best_idx}, Dist={best_dist:.6f}")

    if top_result[0] == best_idx:
        print("✅ Correctness passed.")
    else:
        print("⚠️ Correctness warning: Top result ID mismatch (could be tied scores).")

if __name__ == "__main__":
    benchmark()
