## 2024-05-22 - Optimizing OllamaClient Connection Reuse
**Learning:** `requests.post` creates a new connection for every call, adding significant latency (TCP handshake) for high-frequency API calls like LLM generation streaming. Using `requests.Session` enables connection pooling (keep-alive).
**Action:** Always use `requests.Session` for clients that make repeated requests to the same host. Verify with mock tests checking `session.post` calls vs module-level `requests.post`.
