"""Tests for tdd_enforcer hook."""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent to path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from tdd_enforcer import has_test_file, is_test_file, is_trivial_edit, should_skip


class TestShouldSkip:
    def test_skip_markdown(self) -> None:
        assert should_skip("README.md") is True

    def test_skip_json(self) -> None:
        assert should_skip("package.json") is True

    def test_skip_yaml(self) -> None:
        assert should_skip("config.yaml") is True

    def test_skip_lock(self) -> None:
        assert should_skip("poetry.lock") is True

    def test_skip_migrations_dir(self) -> None:
        assert should_skip("/app/migrations/0001_initial.py") is True

    def test_skip_generated_dir(self) -> None:
        assert should_skip("/app/generated/schema.ts") is True

    def test_skip_node_modules(self) -> None:
        assert should_skip("/project/node_modules/pkg/index.js") is True

    def test_skip_init_py(self) -> None:
        assert should_skip("app/__init__.py") is True

    def test_no_skip_python(self) -> None:
        assert should_skip("app/models.py") is False

    def test_no_skip_typescript(self) -> None:
        assert should_skip("src/App.tsx") is False

    def test_no_skip_go(self) -> None:
        assert should_skip("cmd/main.go") is False


class TestIsTestFile:
    def test_python_test_prefix(self) -> None:
        assert is_test_file("tests/test_models.py") is True

    def test_python_test_suffix(self) -> None:
        assert is_test_file("tests/models_test.py") is True

    def test_python_impl(self) -> None:
        assert is_test_file("app/models.py") is False

    def test_ts_test(self) -> None:
        assert is_test_file("src/App.test.ts") is True

    def test_tsx_spec(self) -> None:
        assert is_test_file("src/App.spec.tsx") is True

    def test_js_test(self) -> None:
        assert is_test_file("src/utils.test.js") is True

    def test_ts_impl(self) -> None:
        assert is_test_file("src/App.ts") is False

    def test_go_test(self) -> None:
        assert is_test_file("pkg/handler_test.go") is True

    def test_go_impl(self) -> None:
        assert is_test_file("pkg/handler.go") is False

    def test_dunder_tests_dir(self) -> None:
        assert is_test_file("src/__tests__/App.tsx") is True


class TestIsTrivialEdit:
    def test_non_edit_tool(self) -> None:
        assert is_trivial_edit("Write", {"old_string": "x", "new_string": "y"}) is False

    def test_import_only_change(self) -> None:
        assert is_trivial_edit(
            "Edit",
            {
                "old_string": "import os",
                "new_string": "import os\nimport sys",
            },
        ) is True

    def test_constant_addition(self) -> None:
        assert is_trivial_edit(
            "Edit",
            {
                "old_string": "MAX_SIZE = 100",
                "new_string": "MAX_SIZE = 100\nDEFAULT_TIMEOUT = 30",
            },
        ) is True

    def test_removal_only(self) -> None:
        assert is_trivial_edit(
            "Edit",
            {
                "old_string": "line1\nline2\nline3",
                "new_string": "line1\nline3",
            },
        ) is True

    def test_non_trivial_edit(self) -> None:
        assert is_trivial_edit(
            "Edit",
            {
                "old_string": "def foo(): pass",
                "new_string": "def foo():\n    return 42",
            },
        ) is False

    def test_empty_strings(self) -> None:
        assert is_trivial_edit("Edit", {"old_string": "", "new_string": ""}) is False


class TestHasTestFile:
    def test_python_sibling_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "models.py"
        impl.write_text("class User: pass")
        test = tmp_path / "test_models.py"
        test.write_text("def test_user(): pass")
        assert has_test_file(str(impl)) is True

    def test_python_no_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "models.py"
        impl.write_text("class User: pass")
        assert has_test_file(str(impl)) is False

    def test_ts_sibling_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "App.ts"
        impl.write_text("export default {}")
        test = tmp_path / "App.test.ts"
        test.write_text("test('app', () => {})")
        assert has_test_file(str(impl)) is True

    def test_ts_no_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "App.ts"
        impl.write_text("export default {}")
        assert has_test_file(str(impl)) is False

    def test_go_sibling_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "handler.go"
        impl.write_text("package main")
        test = tmp_path / "handler_test.go"
        test.write_text("package main")
        assert has_test_file(str(impl)) is True

    def test_go_no_test(self, tmp_path: Path) -> None:
        impl = tmp_path / "handler.go"
        impl.write_text("package main")
        assert has_test_file(str(impl)) is False

    def test_python_test_in_tests_dir(self, tmp_path: Path) -> None:
        src = tmp_path / "src"
        src.mkdir()
        impl = src / "models.py"
        impl.write_text("class User: pass")
        tests = tmp_path / "tests"
        tests.mkdir()
        test = tests / "test_models.py"
        test.write_text("def test_user(): pass")
        assert has_test_file(str(impl)) is True
