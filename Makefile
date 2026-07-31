.PHONY: help smoke test verify clean install

help:
	@echo "make install  — Install dependencies with uv"
	@echo "make test     — Run full test suite"
	@echo "make smoke    — Run smoke workflow (8 steps)"
	@echo "make verify   — Run all verification scripts"
	@echo "make clean    — Remove __pycache__, .pyc, logs"

install:
	uv sync

test:
	uv run pytest -v --tb=short

smoke:
	bash scripts/agentic/run_smoke_workflow.sh

verify:
	bash scripts/agentic/verify_proxy.sh --tier all
	bash scripts/agentic/verify_task_spine.sh
	bash scripts/agentic/verify_worker_runtime.sh --workers 1

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	rm -rf logs/ tmp/
