#!/usr/bin/env python3
"""PostToolUse hook: TDD reminder when implementation files edited without tests.

Non-blocking reminder (exit 0 + systemMessage). Edits always complete,
then a reminder is shown to encourage TDD practices.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin

EXCLUDED_EXTENSIONS = {
    ".md", ".rst", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".lock", ".sum", ".env", ".sql",
}

EXCLUDED_DIRS = {
    "/cdk/", "/infra/", "/infrastructure/", "/terraform/", "/pulumi/",
    "/stacks/", "/cloudformation/", "/deploy/", "/migrations/", "/alembic/",
    "/generated/", "/proto/", "/__generated__/", "/dist/", "/build/",
    "/node_modules/", "/.venv/", "/venv/", "/__pycache__/",
}


def should_skip(file_path: str) -> bool:
    """Check if file should be skipped based on extension or directory."""
    path = Path(file_path)

    if path.suffix in EXCLUDED_EXTENSIONS:
        return True
    if path.name in EXCLUDED_EXTENSIONS:
        return True
    if path.name == "__init__.py":
        return True

    for excluded_dir in EXCLUDED_DIRS:
        if excluded_dir in file_path:
            return True

    return False


def is_test_file(file_path: str) -> bool:
    """Check if file is a test file."""
    name = Path(file_path).name

    if name.endswith(".py"):
        stem = Path(file_path).stem
        if stem.startswith("test_") or stem.endswith("_test"):
            return True

    if name.endswith((".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx",
                      ".test.js", ".spec.js", ".test.jsx", ".spec.jsx")):
        return True

    if name.endswith("_test.go"):
        return True

    dir_path = Path(file_path).parent.as_posix()
    if "/__tests__/" in dir_path or dir_path.endswith("/__tests__"):
        return True

    return False


def is_trivial_edit(tool_name: str, tool_input: dict) -> bool:
    """Check if an Edit is trivial (imports, constants, removals)."""
    if tool_name != "Edit":
        return False

    old_string = tool_input.get("old_string", "")
    new_string = tool_input.get("new_string", "")

    if not old_string or not new_string:
        return False

    old_lines = [line.strip() for line in old_string.strip().splitlines() if line.strip()]
    new_lines = [line.strip() for line in new_string.strip().splitlines() if line.strip()]

    if not old_lines and not new_lines:
        return False

    # Import-only changes
    all_lines = old_lines + new_lines
    if all_lines and all(_is_import_line(line) for line in all_lines):
        return True

    # Removal-only (new is subsequence of old)
    if new_lines and len(new_lines) < len(old_lines):
        it = iter(old_lines)
        if all(line in it for line in new_lines):
            return True

    # Constant additions only (UPPER_CASE = ...)
    import re
    added = [line for line in new_lines if line not in old_lines]
    removed = [line for line in old_lines if line not in new_lines]
    if added and not removed and all(re.match(r"^[A-Z][A-Z_0-9]*\s*=\s*", line) for line in added):
        return True

    return False


def _is_import_line(line: str) -> bool:
    """Check if a line is an import statement."""
    return line.startswith(("import ", "from ", "const ", "let ", "var ")) and (
        " from " in line or "import " in line or "require(" in line
    )


def _find_test_dirs(start: Path) -> list[Path]:
    """Walk up from start to find common test directories."""
    dirs: list[Path] = []
    current = start
    for _ in range(15):
        for name in ("tests", "test", "__tests__"):
            candidate = current / name
            if candidate.is_dir():
                dirs.append(candidate)
        if current.parent == current:
            break
        current = current.parent
    return dirs


def _search_test_dirs_prefix(test_dirs: list[Path], prefix: str, extensions: list[str]) -> bool:
    """Search test dirs for files whose name starts with prefix.

    Handles cases like VaultAssetDetail.tsx in Vault/ matching vault-view.test.ts.
    Converts CamelCase prefix to kebab-case for matching.
    """
    import re
    # Convert CamelCase to kebab-case for broader matching
    kebab = re.sub(r"(?<=[a-z])(?=[A-Z])", "-", prefix).lower()
    prefixes = {prefix.lower(), kebab}

    for test_dir in test_dirs:
        try:
            for f in test_dir.rglob("*"):
                if not f.is_file():
                    continue
                fname = f.stem.lower()
                # Strip test suffixes to get the base name
                for suffix in (".test", ".spec", "_test", "test_"):
                    if fname.endswith(suffix):
                        fname = fname[: -len(suffix)]
                    if fname.startswith(suffix):
                        fname = fname[len(suffix):]
                for p in prefixes:
                    if fname.startswith(p) or p.startswith(fname):
                        return True
        except OSError:
            continue
    return False


def has_related_failing_test(project_dir: str, impl_file: str) -> bool:
    """Check if there's a failing test specifically for this module in pytest cache."""
    cache_file = Path(project_dir) / ".pytest_cache" / "v" / "cache" / "lastfailed"
    if not cache_file.exists():
        return False

    module_name = Path(impl_file).stem

    try:
        lastfailed = json.loads(cache_file.read_text())
        if not lastfailed:
            return False

        for test_path in lastfailed:
            test_file = test_path.split("::")[0]
            test_name = Path(test_file).stem
            if test_name == f"test_{module_name}" or test_name == f"{module_name}_test":
                return True

        return False
    except (json.JSONDecodeError, OSError):
        return False


def has_test_file(impl_path: str) -> bool:
    """Check if a corresponding test file exists for the given implementation file."""
    path = Path(impl_path)
    ext = path.suffix

    if ext == ".py":
        module_name = path.stem
        sibling_names = [f"test_{module_name}.py", f"{module_name}_test.py"]
        for name in sibling_names:
            if (path.parent / name).exists():
                return True
        test_dirs = _find_test_dirs(path.parent)
        for test_dir in test_dirs:
            for pattern in [f"**/test_{module_name}.py", f"**/{module_name}_test.py"]:
                if list(test_dir.glob(pattern)):
                    return True
        # Try parent-dir prefix matching
        parent_name = path.parent.name
        if parent_name and _search_test_dirs_prefix(test_dirs, parent_name, [".py"]):
            return True
        return False

    if ext in (".ts", ".tsx", ".js", ".jsx"):
        if ext in (".tsx", ".jsx"):
            base_name = path.name[: -(len(ext))]
            extensions = [".test" + ext, ".spec" + ext, ".test.ts", ".spec.ts"]
        else:
            base_name = path.stem
            extensions = [".test" + ext, ".spec" + ext]

        # Check siblings
        for test_ext in extensions:
            if (path.parent / f"{base_name}{test_ext}").exists():
                return True

        # Check test directories
        test_dirs = _find_test_dirs(path.parent)
        for test_dir in test_dirs:
            for test_ext in extensions:
                if list(test_dir.glob(f"**/{base_name}{test_ext}")):
                    return True

        # Check __tests__ directory
        tests_dir = path.parent / "__tests__"
        if tests_dir.is_dir():
            for f in tests_dir.iterdir():
                if base_name in f.name:
                    return True

        # Try parent-dir prefix matching
        parent_name = path.parent.name
        if parent_name and test_dirs and _search_test_dirs_prefix(test_dirs, parent_name, list(extensions)):
            return True

        return False

    if ext == ".go":
        base_name = path.stem
        if (path.parent / f"{base_name}_test.go").exists():
            return True
        test_dirs = _find_test_dirs(path.parent)
        for test_dir in test_dirs:
            if list(test_dir.glob(f"**/{base_name}_test.go")):
                return True
        return False

    return False


def warn(message: str, suggestion: str) -> None:
    """Output TDD warning as JSON systemMessage."""
    print(
        json.dumps(
            {
                "systemMessage": f"TDD: {message}. {suggestion}",
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": "TDD reminder: RED -> GREEN -> REFACTOR",
                },
            }
        )
    )


def check(data: dict) -> str | None:
    """Check if the edited file needs a TDD reminder.

    Accepts the parsed hook stdin data dict. Returns the TDD warning
    message string if a reminder is warranted, or None.
    """
    if not data:
        return None

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        return None

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
    if not file_path:
        return None

    if should_skip(file_path):
        return None

    if is_test_file(file_path):
        return None

    if is_trivial_edit(tool_name, tool_input if isinstance(tool_input, dict) else {}):
        return None

    # Check for failing tests (Python only - uses pytest cache)
    if file_path.endswith(".py"):
        path = Path(file_path).parent
        for _ in range(10):
            if has_related_failing_test(str(path), file_path):
                return None
            if path.parent == path:
                break
            path = path.parent

    if not has_test_file(file_path):
        ext = Path(file_path).suffix
        base = Path(file_path).stem
        if ext == ".py":
            return f"TDD: No test file found for '{base}' module. Consider creating test_{base}.py first."
        elif ext in (".ts", ".tsx"):
            return f"TDD: No test file found for this module. Consider creating {base}.test.ts first."
        elif ext == ".go":
            return f"TDD: No test file found. Consider creating {base}_test.go first."

    return None


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    result = check(data)
    if result:
        print(
            json.dumps(
                {
                    "systemMessage": result,
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": "TDD reminder: RED -> GREEN -> REFACTOR",
                    },
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
