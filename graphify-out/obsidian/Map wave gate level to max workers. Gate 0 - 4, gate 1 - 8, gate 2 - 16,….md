---
source_file: "src/merged_agentic_swarm/services/opencode_swarm_service.py"
type: "rationale"
community: "ConcurrencyRampController"
location: "L300"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/ConcurrencyRampController
---

# Map wave gate level to max workers. Gate 0 -> 4, gate 1 -> 8, gate 2 -> 16,…

## Connections
- [[dot-get_current_max_workers()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/ConcurrencyRampController