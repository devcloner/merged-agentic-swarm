---
source_file: "tests/test_streaming_proxy.py"
type: "rationale"
community: "_StallStream"
location: "L122"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/_StallStream
---

# Consume (or close) a StreamingResponse so upstream streams are torn down.

## Connections
- [[drain()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/_StallStream