
import sys
import os
import numpy as np

# Add repo root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from memory.lightweight_vector_db import HNSWIndex

def verify_correctness():
    print("🧪 Verifying HNSWIndex correctness...")

    # 3 dimensions for easy manual verification
    index = HNSWIndex(dimension=3)

    # Vectors
    # v1 is unit vector on X
    v1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    # v2 is unit vector on Y
    v2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    # v3 is 45 degrees between X and Y
    v3 = np.array([1.0, 1.0, 0.0], dtype=np.float32)
    v3 = v3 / np.linalg.norm(v3) # Normalize v3 -> [0.707, 0.707, 0]

    # Add vectors
    index.add(1, v1)
    index.add(2, v2)
    index.add(3, v3)

    # Search for v1
    query = v1
    results = index.search(query, k=3)

    print("Results for searching v1:")
    for id, dist in results:
        print(f"  ID: {id}, Dist: {dist:.4f}")

    # Validation
    # Top result should be ID 1 with distance ~0
    assert results[0][0] == 1
    assert abs(results[0][1]) < 1e-6, f"Expected distance 0, got {results[0][1]}"

    # Second result should be ID 3 with distance 1 - cos(45) = 1 - 0.707 = 0.293
    expected_dist_v3 = 1 - np.dot(v1, v3)
    assert results[1][0] == 3
    assert abs(results[1][1] - expected_dist_v3) < 1e-6, f"Expected {expected_dist_v3}, got {results[1][1]}"

    # Third result should be ID 2 with distance 1 - cos(90) = 1 - 0 = 1
    assert results[2][0] == 2
    assert abs(results[2][1] - 1.0) < 1e-6, f"Expected 1.0, got {results[2][1]}"

    print("✅ Correctness verification passed!")

if __name__ == "__main__":
    verify_correctness()
