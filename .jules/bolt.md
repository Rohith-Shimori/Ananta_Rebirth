## 2024-05-23 - Runtime Data Persistence
**Learning:** Runtime-generated files in `data/` (like `vector_db/`) are tracked in git but modified by tests.
**Action:** Always revert changes to `data/` files after running tests, or exclude them from commits.
