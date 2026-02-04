
import unittest
import numpy as np
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.lightweight_vector_db import HNSWIndex

class TestHNSWCorrectness(unittest.TestCase):
    def test_search_correctness(self):
        dimension = 3
        index = HNSWIndex(dimension=dimension)

        # Define vectors
        # v1: aligned with x-axis
        v1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        # v2: aligned with y-axis
        v2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        # v3: 45 degrees between x and y
        v3 = np.array([1.0, 1.0, 0.0], dtype=np.float32)
        # Note: v3 is not normalized here, but cosine similarity should handle it

        # Add to index
        index.add(1, v1)
        index.add(2, v2)
        index.add(3, v3)

        # Query: slightly off x-axis towards y
        # Should be closest to v1, then v3, then v2
        query = np.array([10.0, 1.0, 0.0], dtype=np.float32) # Magnitude shouldn't matter

        results = index.search(query, k=3)

        # Check IDs
        ids = [r[0] for r in results]
        self.assertEqual(ids, [1, 3, 2], f"Expected order [1, 3, 2], got {ids}")

        # Check distances
        # Dist to v1 should be very small
        dist_v1 = results[0][1]
        self.assertTrue(dist_v1 < 0.1, f"Distance to v1 {dist_v1} should be small")

        # Dist to v2 should be large (near 1.0 approx)
        dist_v2 = results[2][1]
        self.assertTrue(dist_v2 > 0.5, f"Distance to v2 {dist_v2} should be large")

    def test_empty_search(self):
        index = HNSWIndex(dimension=3)
        results = index.search(np.array([1, 0, 0]), k=5)
        self.assertEqual(results, [])

    def test_add_after_search(self):
        # Test that adding a vector after a search invalidates the cache correctly
        index = HNSWIndex(dimension=3)
        index.add(1, np.array([1.0, 0.0, 0.0], dtype=np.float32))

        # Search 1
        results = index.search(np.array([1.0, 0.0, 0.0]), k=1)
        self.assertEqual(results[0][0], 1)

        # Add new vector
        index.add(2, np.array([0.0, 1.0, 0.0], dtype=np.float32))

        # Search 2 (should find both or correct one)
        # Query matching vector 2
        results = index.search(np.array([0.0, 1.0, 0.0]), k=1)
        self.assertEqual(results[0][0], 2)

if __name__ == '__main__':
    unittest.main()
