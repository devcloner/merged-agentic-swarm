---
source_file: "tests/test_fast_fallback.py"
type: "rationale"
community: "_router_with_keys"
location: "L160"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/_router_with_keys
---

# A losing in-flight probe (2xx after another probe won) must not corrupt state.

## Connections
- [[dot-test_loser_records_no_spurious_failure()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/_router_with_keys