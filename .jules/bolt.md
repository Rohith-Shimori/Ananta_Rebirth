# Bolt's Journal

## 2024-05-23 - Vector Search Bottleneck
**Learning:** `LightweightVectorDB` was using a naive Python loop for cosine similarity search. This is O(N) but with a large constant factor due to Python overhead and repeated `np.linalg.norm` calls.
**Action:** Always vectorize numerical operations with NumPy. Avoid loops for distance calculations. Use matrix multiplication (`matrix @ vector`) for batch similarity.
