## 2024-05-23 - Vector Search Optimization
**Learning:** Iterative cosine distance calculation in Python for 10k vectors is extremely slow (~0.08s). Vectorizing with `np.dot` improves it by ~200x (~0.0004s).
**Action:** Always check for opportunities to replace loops with matrix operations in numerical code. Ensure vectors are normalized when using dot product for cosine similarity.
