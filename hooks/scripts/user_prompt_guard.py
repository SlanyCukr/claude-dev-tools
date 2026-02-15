#!/usr/bin/env python3
"""UserPromptSubmit hook: catch requests that bypass quality standards.

Detects prompts that explicitly ask to skip tests, ignore linting,
or avoid code review. Sends a non-blocking reminder (exit 0 + systemMessage).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin

# Patterns that suggest bypassing quality standards
BYPASS_PATTERNS = [
    (
        r"(?:skip|without|no|don'?t|ignore|disable)\s+(?:the\s+)?tests?",
        "Skipping tests violates TDD workflow. Write tests first (RED), then implement (GREEN).",
    ),
    (
        r"(?:skip|without|no|don'?t|ignore|disable)\s+(?:the\s+)?(?:lint|linting|type.?check)",
        "Skipping lint/type checks risks shipping broken code. Fix issues instead.",
    ),
    (
        r"(?:skip|without|no|don'?t|ignore|disable)\s+(?:the\s+)?(?:code\s+)?review",
        "Skipping code review misses bugs. Use /review after implementation.",
    ),
    (
        r"(?:skip|without|no|don'?t|ignore|disable)\s+(?:the\s+)?security",
        "Skipping security checks is dangerous. Use /security for sensitive code.",
    ),
    (
        r"just\s+(?:do|make|write|implement)\s+it\s+(?:fast|quick|without)",
        "Rushing bypasses quality gates. Consider /quick for small well-defined tasks.",
    ),
]


def check(data: dict) -> str | None:
    """Check user prompt for quality bypass patterns.

    Returns a reminder message if bypass detected, or None.
    """
    prompt = data.get("user_prompt", "")
    if not prompt:
        return None

    for pattern, reminder in BYPASS_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return reminder

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
                    "systemMessage": f"Quality reminder: {result}",
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": "Quality standards enforced by plugin.",
                    },
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
