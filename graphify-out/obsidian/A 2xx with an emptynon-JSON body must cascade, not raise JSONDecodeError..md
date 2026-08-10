---
source_file: "tests/test_multi_provider_fabric.py"
type: "rationale"
community: "TestDispatchRequest"
location: "L356"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/TestDispatchRequest
---

# A 2xx with an empty/non-JSON body must cascade, not raise JSONDecodeError.

## Connections
- [[dot-test_dispatch_non_json_body_falls_through()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/TestDispatchRequest