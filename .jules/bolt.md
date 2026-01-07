## 2026-01-07 - Persistent SQLite Connection
**Learning:** SQLite connection overhead is significant for high-frequency operations. Keeping a persistent connection with `check_same_thread=False` (if safe) yielded a 5x improvement in read performance.
**Action:** Always consider connection pooling or persistent connections for local DBs in high-frequency paths.
