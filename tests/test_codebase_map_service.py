"""
Tests for services/codebase_map_service.py

Coverage: CodebaseMapService — scan_repository, detect_spec_gaps,
close_spec_gap, _parse_python_ast.
"""
import os

from models.prd_models import SpecGap


class TestCodebaseMapService:
    def test_scan_empty_repo(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        result = mapper.scan_repository()
        assert result["total_files"] == 0
        assert result["python_files"] == 0

    def test_scan_repo_with_python_file(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        # Create a Python file in temp_dir
        subdir = os.path.join(temp_dir, "services")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "test_module.py"), "w") as f:
            f.write("class TestClass:\n    pass\n\ndef test_func():\n    pass\n")

        mapper = CodebaseMapService(repo_root=temp_dir)
        result = mapper.scan_repository()
        assert result["total_files"] >= 1
        assert result["python_files"] >= 1

    def test_scan_preserves_state_file(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        mapper.scan_repository()
        state_path = mapper._state_file
        assert os.path.exists(state_path)

    def test_load_from_cache(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper1 = CodebaseMapService(repo_root=temp_dir)
        mapper1.scan_repository()

        mapper2 = CodebaseMapService(repo_root=temp_dir)
        assert mapper2.symbol_cache.get("total_files") is not None

    def test_detect_spec_gaps_no_gaps(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        # Create the required component
        os.makedirs(os.path.join(temp_dir, "models"))
        gaps = mapper.detect_spec_gaps(required_components=["models"])
        assert len(gaps) == 0

    def test_detect_spec_gaps_with_gaps(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        gaps = mapper.detect_spec_gaps(required_components=["nonexistent_component"])
        assert len(gaps) == 1
        assert gaps[0].id == "GAP-01"
        assert "nonexistent_component" in gaps[0].missing_requirement

    def test_close_spec_gap(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        mapper.spec_gaps = [
            SpecGap(
                id="GAP-01", epic_id="EPIC-00",
                missing_requirement="X", affected_files=["x.py"],
                suggested_fix="Add X",
            )
        ]
        result = mapper.close_spec_gap("GAP-01", "Created x.py")
        assert result is True
        assert mapper.spec_gaps[0].resolved

    def test_close_spec_gap_not_found(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        result = mapper.close_spec_gap("GAP-MISSING", "note")
        assert result is False

    def test_parse_python_ast_extracts_symbols(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        file_path = os.path.join(temp_dir, "example.py")
        with open(file_path, "w") as f:
            f.write("""
import os
from typing import List

class MyClass:
    pass

def my_func():
    pass
""")
        symbols = mapper._parse_python_ast(file_path)
        assert "MyClass" in symbols.get("classes", [])
        assert "my_func" in symbols.get("functions", [])
        assert "os" in symbols.get("imports", [])

    def test_parse_invalid_file(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        symbols = mapper._parse_python_ast(os.path.join(temp_dir, "nonexistent.py"))
        assert "error" in symbols

    def test_detect_hidden_directory(self, temp_dir):
        from services.codebase_map_service import CodebaseMapService
        mapper = CodebaseMapService(repo_root=temp_dir)
        os.makedirs(os.path.join(temp_dir, ".opencode"))
        gaps = mapper.detect_spec_gaps(required_components=["opencode"])
        assert len(gaps) == 0  # hidden dir is found
