#!/usr/bin/env python3
"""PostToolUse hook: modular linter with auto-fix, type checking, and file length warnings."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _checkers import is_test_file
from _checkers import python as py_checker
from _checkers import typescript as ts_checker
from _checkers import go as go_checker
from _util import check_file_length, find_git_root, get_edited_file_from_stdin

CHECKER_MAP = {
    ".py": py_checker.check,
    ".ts": ts_checker.check,
    ".tsx": ts_checker.check,
    ".js": ts_checker.check,
    ".jsx": ts_checker.check,
    ".go": go_checker.check,
}


def check(data: dict) -> str | None:
    """Run lint/type checks on the edited file.

    Accepts the parsed hook stdin data dict. Returns the systemMessage
    string when issues are found, or None.

    Saves and restores the working directory since linters need to run
    from the git root.
    """
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
    if not file_path:
        return None

    saved_cwd = os.getcwd()
    try:
        # chdir to git root so linters resolve their configs correctly
        git_root = find_git_root(Path(file_path).parent)
        if git_root:
            os.chdir(git_root)

        ext = Path(file_path).suffix
        checker = CHECKER_MAP.get(ext)
        if not checker:
            return None

        if is_test_file(file_path):
            return None

        # Run language checker
        results = checker(file_path)

        # Check file length
        length_check = check_file_length(file_path)

        # Build output
        parts: list[str] = []
        for r in results:
            s = r.summary()
            if s:
                parts.append(s)

        if length_check:
            level, lines = length_check
            if level == "critical":
                parts.append(f"[file-length] CRITICAL: {lines} lines — split this file")
            else:
                parts.append(f"[file-length] Warning: {lines} lines — consider splitting")

        if parts:
            return "\n\n".join(parts)
        return None
    finally:
        os.chdir(saved_cwd)


def main() -> int:
    data, file_path = get_edited_file_from_stdin()
    if not file_path:
        return 0

    result = check(data)
    if result:
        print(
            json.dumps(
                {
                    "systemMessage": result,
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": "Lint/type errors found. Fix before committing.",
                    },
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
