---
source_file: "tests/test_streaming_proxy.py"
type: "rationale"
community: "test_streaming_proxy.py"
location: "L525"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/test_streaming_proxypy
---

# All requests share one httpx.AsyncClient (connection pooling).

## Connections
- [[test_connection_reuse_single_pooled_client()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/test_streaming_proxypy