"""
Codebase Mapper & Spec Gap Closer Service
Maps repository structure, AST symbols, and closes spec gaps before mass edits.
"""

import ast
import fnmatch
import json
import logging
import os
from typing import Any

from merged_agentic_swarm.models.prd_models import SpecGap

logger = logging.getLogger("codebase_map_service")


class CodebaseMapService:
    def __init__(self, repo_root: str | None = None):
        if repo_root is None:
            repo_root = os.getcwd()
        self.repo_root = repo_root
        self.symbol_cache: dict[str, Any] = {}
        self.spec_gaps: list[SpecGap] = []
        self._state_file: str = os.path.join(repo_root, ".opencode", "codebase_cache.json")
        self._ignore_dirs = {
            ".git",
            "node_modules",
            ".cache",
            ".cargo",
            ".rustup",
            "__pycache__",
            ".npm",
            ".gemini",
            ".local",
            "snap",
            ".atomic",
            ".aws",
            ".cloudcli",
            ".codex",
            ".config",
            ".cursor",
            ".docker",
            ".fcc",
            ".fcc-tmp",
            ".omo",
            ".pi",
            ".remember",
            ".serena",
            "claudecodeui",
            "Spotify-project-main",
            "venv",
            ".venv",
            "build",
            "dist",
            "target",
            "vendor",
            "site-packages",
        }
        self._ignore_patterns: list[tuple[str, bool]] = []
        self._ignore_negations: list[tuple[str, bool]] = []
        self._load_gitignore()
        self._load_state()

    def _load_gitignore(self) -> None:
        """Load the repo-root .gitignore into (pattern, dir_only) matcher lists.

        Covers the common gitignore forms: comments, `!` negation, trailing `/`
        (directory-only), and slash-anchored vs basename patterns. Full gitignore
        semantics (nested .gitignore files, ** globs) are out of scope.
        """
        path = os.path.join(self.repo_root, ".gitignore")
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.rstrip("\n").rstrip()
                if not line or line.startswith("#"):
                    continue
                negate = line.startswith("!")
                if negate:
                    line = line[1:].lstrip()
                dir_only = line.endswith("/")
                pattern = line.rstrip("/")
                if not pattern:
                    continue
                target = self._ignore_negations if negate else self._ignore_patterns
                target.append((pattern, dir_only))

    def _is_gitignored(self, rel: str, is_dir: bool) -> bool:
        if not self._ignore_patterns and not self._ignore_negations:
            return False
        matched = False
        for pattern, dir_only in self._ignore_patterns:
            if dir_only and not is_dir:
                continue
            if self._pattern_matches(pattern, rel):
                matched = True
                break
        if matched:
            for pattern, dir_only in self._ignore_negations:
                if dir_only and not is_dir:
                    continue
                if self._pattern_matches(pattern, rel):
                    return False
        return matched

    @staticmethod
    def _pattern_matches(pattern: str, rel: str) -> bool:
        if "/" in pattern:
            return fnmatch.fnmatch(rel, pattern)
        return fnmatch.fnmatch(os.path.basename(rel), pattern)

    def _is_ignored_path(self, full_path: str, is_dir: bool) -> bool:
        name = os.path.basename(full_path)
        if is_dir and (name in self._ignore_dirs or name.startswith(".") or os.path.islink(full_path)):
            return True
        rel = os.path.relpath(full_path, self.repo_root).replace(os.sep, "/")
        return self._is_gitignored(rel, is_dir)

    def scan_repository(self) -> dict[str, Any]:
        """Scans workspace repository files and parses AST definitions."""
        file_tree = []
        symbol_index = {}

        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if not self._is_ignored_path(os.path.join(root, d), is_dir=True)]
            try:
                for file in files:
                    full_path = os.path.join(root, file)
                    if self._is_ignored_path(full_path, is_dir=False):
                        continue
                    rel_path = os.path.relpath(full_path, self.repo_root)
                    file_tree.append(rel_path)

                    if file.endswith(".py"):
                        symbols = self._parse_python_ast(full_path)
                        if symbols:
                            symbol_index[rel_path] = symbols
            except PermissionError:
                logger.debug(f"Permission denied scanning {root}, skipping.")
                continue

        # Store up to FILE_LIST_MAX entries so spec-gap detection has broad
        # coverage; large repos won't miss components due to truncation.
        FILE_LIST_MAX = 10_000
        self.symbol_cache = {
            "total_files": len(file_tree),
            "python_files": len(symbol_index),
            "file_list": file_tree[:FILE_LIST_MAX],
            "symbols": symbol_index,
        }
        self._save_state()
        logger.info(f"Codebase map completed: {len(file_tree)} total files, {len(symbol_index)} python modules parsed.")
        return self.symbol_cache

    def _parse_python_ast(self, file_path: str) -> dict[str, Any]:
        """Parses Python file to extract top-level functions, classes, and imports."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            tree = ast.parse(code, filename=file_path)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)

            return {"classes": classes, "functions": functions, "imports": list(set(imports))}
        except Exception as e:
            return {"error": str(e)}

    def detect_spec_gaps(self, required_components: list[str]) -> list[SpecGap]:
        """Cross-references required components against mapped codebase to find spec gaps.

        Checks whether each required component exists as a directory or file in the
        repository root, rather than relying on naive filename suffix matching.
        """
        self.scan_repository()
        gaps = []

        for comp in required_components:
            # Check directory existence first (e.g. 'services/' → services/)
            dir_path = os.path.join(self.repo_root, comp)
            # Check hidden directory (e.g. 'opencode' → '.opencode/')
            hidden_dir_path = os.path.join(self.repo_root, f".{comp}")
            # Check file existence (e.g. 'opencode-swarm.json')
            file_path = os.path.join(self.repo_root, comp)
            # Check if any existing file path contains the component as a segment
            existing_files = self.symbol_cache.get("file_list", [])
            path_in_filelist = any(f"/{comp}/" in f or f.startswith(f"{comp}/") for f in existing_files)

            if (
                os.path.isdir(dir_path)
                or os.path.isdir(hidden_dir_path)
                or os.path.isfile(file_path)
                or path_in_filelist
            ):
                continue  # component exists — no gap

            gap = SpecGap(
                id=f"GAP-{len(gaps) + 1:02d}",
                epic_id="EPIC-00",
                missing_requirement=f"Component '{comp}' missing from mapped codebase",
                affected_files=[f"{comp}/"],
                suggested_fix=f"Bootstrap directory {comp}/ with standard service interface.",
            )
            gaps.append(gap)

        self.spec_gaps = gaps
        logger.info(f"Detected {len(gaps)} spec gaps during codebase pre-mapping.")
        return gaps

    def _load_state(self) -> None:
        """Load persisted codebase map state from disk."""
        if os.path.exists(self._state_file):
            try:
                with open(self._state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.symbol_cache = data.get("symbol_cache", {})
                logger.info(
                    f"Loaded codebase map from cache: {self.symbol_cache.get('total_files', 0)} files, "
                    f"{self.symbol_cache.get('python_files', 0)} modules"
                )
            except Exception as e:
                logger.warning(f"Could not load codebase map state: {e}")

    def _save_state(self) -> None:
        """Persist codebase map state so restart doesn't require re-scan."""
        try:
            os.makedirs(os.path.dirname(self._state_file), exist_ok=True)
            with open(self._state_file, "w", encoding="utf-8") as f:
                json.dump({"symbol_cache": self.symbol_cache}, f, indent=2)
            logger.info(f"Saved codebase map state to {self._state_file}")
        except Exception as e:
            logger.warning(f"Could not save codebase map state: {e}")

    def close_spec_gap(self, gap_id: str, resolution_note: str) -> bool:
        """Closes a specific spec gap after verifying fixes."""
        for gap in self.spec_gaps:
            if gap.id == gap_id:
                gap.resolved = True
                gap.resolution_note = resolution_note
                logger.info(f"Closed spec gap {gap_id}: {resolution_note}")
                return True
        return False


# Global Singleton
default_codebase_mapper = CodebaseMapService()
