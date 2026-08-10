---
source_file: "tests/test_progress_ledger_service.py"
type: "rationale"
community: "ProgressLedgerService"
location: "L177"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/ProgressLedgerService
---

# Concurrent save_ledger calls must never leave a torn JSON target.

## Connections
- [[dot-test_concurrent_save_ledger_produces_complete_json()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/ProgressLedgerService