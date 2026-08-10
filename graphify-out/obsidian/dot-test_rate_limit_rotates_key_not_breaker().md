---
source_file: "tests/test_fast_fallback.py"
type: "code"
community: "_router_with_keys"
location: "L265"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/_router_with_keys
---

# .test_rate_limit_rotates_key_not_breaker()

## Connections
- [[429 cools the key down but does not trip the provider breaker.]] - `rationale_for` [EXTRACTED]
- [[TestCircuitBreaker]] - `method` [EXTRACTED]
- [[_router_with_keys()]] - `calls` [EXTRACTED]
- [[_url_routed()]] - `calls` [EXTRACTED]
- [[patch]] - `references` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/_router_with_keys