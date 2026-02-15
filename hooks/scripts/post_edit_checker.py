#!/usr/bin/env python3
"""PostToolUse orchestrator: reads stdin once and runs all post-edit checks.

Consolidates file_checker, tdd_enforcer, and console_log_warning into a
single process. Each checker exposes a check(data) -> str | None function
that receives the parsed stdin data and returns a message or None.

Always exits 0 (non-blocking).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin

import console_log_warning
import file_checker
import tdd_enforcer


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    messages: list[str] = []

    for checker in (file_checker.check, tdd_enforcer.check, console_log_warning.check):
        result = checker(data)
        if result:
            messages.append(result)

    if messages:
        combined = "\n\n".join(messages)
        print(
            json.dumps(
                {
                    "systemMessage": combined,
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": "Code quality checks completed.",
                    },
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
