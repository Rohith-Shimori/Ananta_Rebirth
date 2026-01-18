# Bolt's Journal

## 2025-05-18 - Optimized AdaptiveMemory with Persistent Connections
**Learning:** SQLite connection overhead in high-frequency operations can be significant. Enabling WAL mode and reusing connections (thread-safely) provided a ~14x speedup for memory operations (4ms -> 0.29ms).
**Action:** Always check database access patterns in hot paths. If `sqlite3.connect` is called frequently, consider connection pooling or a persistent connection with appropriate locking (`threading.RLock`) and `PRAGMA journal_mode=WAL`.
