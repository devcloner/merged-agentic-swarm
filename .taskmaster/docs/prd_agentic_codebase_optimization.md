# PRD: Agentic Codebase Optimization for Spotify AI Analytics

## Target Architecture

Multi-layered agentic swarm integrating Task Master spine, 40-worker OpenCode pools, key-pool proxy, durable agent factory, multi-backend model fabric, knowledge-box → spawn chain, wave gates, and progress ledger.

## Target Codebase

`/home/ubuntu/spotify-ai` — Spotify AI Analytics v0.6.0, FastAPI + PostgreSQL + pgvector.

## Required Work

### EPIC-00: Wave 0 Foundation — Control Plane & System Init
- Initialize system, verify proxy, bootstrap key pool
- Parse this PRD and create task spine
- Map target codebase, detect spec gaps

### EPIC-01: Wave 1 — Provider Fabric & Contract Tests
- 5 cloud LLM providers: AWS Bedrock, Oracle OCI GenAI, Azure OpenAI, GCP Vertex AI, Alibaba Tongyi
- Each needs contract tests: factory creation, config validation, error handling
- Target: 25+ new tests in `tests/test_ai_abstract.py`

### EPIC-02: Wave 2 — Analytics Service Test Suite & Security Hardening
- `analytics/service.py`: 612 lines, 25 public methods, 0 dedicated tests → 30+ new tests
- Wire telemetry record_* calls into LLM, DB, and SSE consumer code
- Fix missing migration files for orphaned models
- Fix PKCE state store: replace in-memory dict with DB-backed

### EPIC-03: Wave 3 — Code Quality & Bug Fixes
- Fix Quiz 5D/4D archetype dimension mismatch
- Replace hardcoded sample data with real DB queries (quiz, compatibility, visualizer)
- Fix CSS duplication and add light mode
- Fix 5 E2E test failures
- Deduplicate _safe_float/_safe_str

### EPIC-04: Wave 4 — Production Hardening
- Add SSE stream tests (critical real-time feature, zero coverage)
- Add PWA support (service worker, manifest)
- Fix Spotify API rate limiting in batch calls

### EPIC-05: Synthesis & Final Reporting
- Run full test suite verification
- Update all documentation
- Generate execution summary
- Auto-compact registries, persist state
