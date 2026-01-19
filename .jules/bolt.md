## 2024-05-23 - SQLite Performance Pattern
**Learning:** Reusing a single `sqlite3` connection with `PRAGMA journal_mode=WAL` provides ~25x speedup over opening/closing connections per operation for write workloads. However, in a multi-threaded Python app, this requires explicit locking (`threading.RLock`) and robust `check_same_thread=False` configuration.
**Action:** Always prefer persistent connections with WAL for SQLite in Python, wrapped in a thread-safe class with proper lifecycle management (open/close).
