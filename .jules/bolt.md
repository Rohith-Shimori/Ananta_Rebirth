## 2026-01-29 - Default DB Path in Tests
**Learning:** `AdaptiveMemory` defaults to the production database path in `__init__`. Running tests (like `test_ananta_quick.py`) without overriding `db_path` writes to the production `memory/data/adaptive_memory.db`, causing accidental binary file modifications in git.
**Action:** When writing tests involving `AdaptiveMemory`, always pass a temporary `db_path` or mock it. When running existing tests, be aware they might touch production data.
