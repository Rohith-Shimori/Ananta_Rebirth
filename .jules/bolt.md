## 2026-02-05 - Vector DB Optimization
**Learning:** The `HNSWIndex` class in `memory/lightweight_vector_db.py` is misnamed; it implements a flat brute-force search. This presented a massive optimization opportunity using vectorized numpy operations.
**Action:** Always check implementation details rather than relying on class names. When optimizing vector search in Python, always prioritize matrix operations over loops.
