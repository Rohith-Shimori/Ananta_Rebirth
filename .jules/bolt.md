## 2024-05-18 - SQLite Connection Overhead
**Learning:** `AdaptiveMemory` was creating a new SQLite connection for every operation (~2.9ms/op). In high-frequency memory access loops, this is a major bottleneck.
**Action:** Use a persistent connection with `check_same_thread=False` and `threading.RLock`. Enable WAL mode (`PRAGMA journal_mode=WAL`) to handle concurrent reads/writes efficiently. Resulted in ~15x speedup (~0.19ms/op).
