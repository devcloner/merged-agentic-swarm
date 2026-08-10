---
source_file: "tests/test_progress_ledger_service.py"
type: "rationale"
community: "ProgressLedgerService"
location: "L152"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/ProgressLedgerService
---

# Regression for #41: temp file must not be the fixed <target>.tmp.

## Connections
- [[dot-test_save_ledger_uses_unique_temp_name()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/ProgressLedgerService