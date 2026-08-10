---
source_file: "tests/test_streaming_proxy.py"
type: "rationale"
community: "test_streaming_proxy.py"
location: "L406"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/test_streaming_proxypy
---

# #39: an upstream that stalls mid-stream must not hang the client forever.

## Connections
- [[test_stalled_upstream_times_out_and_records_failure()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/test_streaming_proxypy