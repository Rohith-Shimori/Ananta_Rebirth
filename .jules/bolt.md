## 2026-01-30 - Vector DB Optimization
**Learning:** `LightweightVectorDB` was implemented with O(N) Python loops for search, despite being named "HNSWIndex" and intended for speed.
**Action:** Always verify "optimized" components with benchmarks. Implemented vectorized NumPy search for ~50x speedup.
