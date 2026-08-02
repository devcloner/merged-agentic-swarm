# Product Requirements Document: Merged Agentic Swarm

## 1. Vision and Goals

The Merged Agentic Swarm aims to be an **autonomous, self-improving software engineering agent**. Its primary goal is to understand user requirements, devise execution plans, orchestrate sub-agents, and perform real-world software development tasks with minimal human intervention. Key objectives include:

-   **Zero-Defect Engineering**: Strive for high code quality, correctness, and root-cause analysis.
-   **High Test Coverage**: Target and achieve at least 97% line coverage for all implemented code.
-   **Real Work Execution**: Perform actual file modifications, command execution, and testing, avoiding mocks or simulations in the core agentic loop.
-   **Multi-Provider LLM Integration**: Seamlessly utilize various LLM providers (Gemini, LiteLLM, Mistral, NVIDIA NIM, etc.) through a pluggable fabric, with intelligent fallback and load balancing.
-   **Efficient Task Management**: Break down complex requirements into manageable epics and subtasks, manage dependencies, and track progress across defined waves.
-   **Extensible Architecture**: Support for specialized agents, custom provider registration, and a flexible workflow system.
-   **Reliable State Management**: Persist project state, agent registries, and PRD analyses for robust execution and continuation.

## 2. Architecture Overview

The Merged Agentic Swarm is composed of several key components:

-   **Core Orchestrator**: Manages the overall project lifecycle, orchestrates waves, and coordinates component interactions.
-   **Task Master Service**: Parses Product Requirement Documents (PRDs) into structured epics and subtasks, manages task states, and handles dependencies. It interfaces with the model fabric for AI-driven PRD analysis.
-   **Multi-Provider Fabric**: Abstracts LLM interactions, providing a unified interface to various LLM providers. It handles request routing, credential management (key pools), response normalization, and fallback mechanisms.
-   **Agentic Worker Loop**: The core execution engine that runs tasks using real tools (file I/O, shell commands) exposed via an OpenAI-formatted API. It operates within a scoped working directory and enforces safety guardrails.
-   **Durable Agent Router**: Matches incoming tasks to specialized, promoted agents based on category and keyword relevance, loading agent definitions from a registry (JSONL and markdown files).
-   **Provider Integration**: Support for numerous LLM providers, including local setups like LiteLLM and FCC Server, managed via a flexible configuration system.
-   **Local Services**: FCC Server (port 8080) and LiteLLM (port 4000) are critical local infrastructure components.

## 3. Workflow

The typical execution flow follows a PRD-driven pipeline:

1.  **PRD Input**: A PRD outlines the desired functionality or fixes.
2.  **Task Decomposition**: The Task Master Service parses the PRD using the model fabric, breaking it down into **Epics**, **Subtasks**, and **Waves** with defined **acceptance criteria**.
3.  **Wave Execution**: The Orchestrator manages the progression through **Wave Gates**. Each wave consists of multiple subtasks.
4.  **Agentic Worker Loop**: For each subtask, an Agentic Worker Loop is initiated. It dispatches requests to the Multi-Provider Fabric.
5.  **Fabric Routing**: The Fabric selects the best LLM provider (based on tier, availability, and routes) to fulfill the request.
6.  **Real Tool Execution**: When the LLM emits tool calls, the Worker Loop executes them in the context of the target repository (real file writes, shell commands).
7.  **Artifact Generation**: Tools produce real artifacts (files, command outputs) which are managed by the Orchestrator.
8.  **Wave Gate Evaluation**: Upon completion of a wave's subtasks, Wave Gates evaluate progress based on acceptance criteria and real artifacts.
9.  **Iteration/Progression**: The workflow advances to the next wave or iterates until all goals are met or thresholds are achieved.

## 4. Key Features

-   **PRD-driven Development**: End-to-end task execution driven by structured PRDs.
-   **Real Tool Execution**: File system operations and shell commands are performed by workers, providing tangible results.
-   **Multi-Provider LLM Fabric**: Supports diverse LLM providers with intelligent routing and fallback.
-   **Durable Agent Discovery**: Matches tasks to specialized agents from a persistent registry.
-   **High Test Coverage**: Adherence to a 97% line coverage target for all code.
-   **Opencode Mode**: An experimental mode for specialized code generation (currently dormant due to credential issues).
-   **Safety Guardrails**: In-place commands are scoped to the working directory, with timeouts and a denylist to prevent host-level damage.

## 5. Constraints

-   **No Mocks/Simulations**: All agentic worker operations must use real tools; simulated responses are hard failures.
-   **Free Tier Usage**: Primarily utilizes free tiers of LLM providers.
-   **Python 3.14+**: Development environment leverages Python 3.14+ and the `uv` package manager exclusively.
-   **Code Quality**: Adherence to DRY, encapsulation, performance, no type ignores, and specific import/migration guidelines.
-   **Versioning**: Semver PATCH bumps for bug fixes/refactors, MINOR for backward-compatible features, MAJOR for breaking changes, managed via `pyproject.toml` and `uv lock`.

## 6. Verification

-   **Live System Runs**: End-to-end testing of PRD workflows, not solely relying on unit tests.
-   **Test Coverage Metrics**: Maintaining >= 97% line coverage.
-   **Workflow Completion**: Successful execution of multi-wave PRD-driven tasks, with real artifacts produced.
-   **LiteLLM Integration**: Verified LiteLLM models are discoverable by the fabric, usable via fcc-server, and picked by swarm workers.
-   **Codebase Health**: Passing all linters (Ruff) and CI checks (`./scripts/ci.sh`).
