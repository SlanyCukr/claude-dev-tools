#!/usr/bin/env python3
"""PostToolUse hook: warn when console.log statements are added to JS/TS files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin


def check(data: dict) -> str | None:
    """Check if the edit introduces console.log statements.

    Accepts the parsed hook stdin data dict. Returns the warning
    message string if console.log is detected, or None.
    """
    if not data:
        return None

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""

    if not re.search(r"\.(js|jsx|ts|tsx|mjs|cjs)$", file_path):
        return None

    new_string = tool_input.get("new_string", "") if isinstance(tool_input, dict) else ""
    content = tool_input.get("content", "") if isinstance(tool_input, dict) else ""
    text = new_string or content
    if "console.log" in text:
        return "console.log detected - remember to remove before commit"

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
                        "additionalContext": result,
                    },
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
