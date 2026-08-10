---
source_file: "tests/test_streaming_proxy.py"
type: "rationale"
community: "test_streaming_proxy.py"
location: "L190"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/test_streaming_proxypy
---

# Proves no-buffering: the first chunk is yielded the instant the upstream writes…

## Connections
- [[test_first_chunk_delivered_before_upstream_emits_rest()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/test_streaming_proxypy