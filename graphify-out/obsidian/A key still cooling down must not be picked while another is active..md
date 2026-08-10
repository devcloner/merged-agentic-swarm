---
source_file: "tests/test_key_pool.py"
type: "rationale"
community: "KeyPoolManager"
location: "L133"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/KeyPoolManager
---

# A key still cooling down must not be picked while another is active.

## Connections
- [[dot-test_get_key_returns_active_key_when_one_in_cooldown()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/KeyPoolManager