#!/usr/bin/env python3
"""PreToolUse hook: block edits containing anti-patterns like backward compatibility or fallbacks."""

import json
import re
import sys

BLOCKED_PATTERNS = [
    (r"backwards?\s+compatibility", "backward compatibility"),
    # Match fallback-as-design-pattern, not variable names or removals
    (
        r"(?:add|provide|use|implement|create|include|keep|with|as)\s+(?:a\s+)?fallback"
        r"|fallback\s+(?:to|for|behavior|mechanism|logic|handling|value|option|strategy|if|when)",
        "fallback mechanism",
    ),
    (r"except\s*:\s*pass", "bare except with pass (exception swallowing)"),
    (r"except\s+Exception\s*:\s*pass", "except Exception with pass (exception swallowing)"),
    (r"\bdeprecated\b", "deprecated (includes @deprecated)"),
    (r"\blegacy\b", "legacy"),
]


def check(data: dict) -> tuple[str, int] | None:
    """Check for anti-patterns in edit content.

    Returns (stderr_message, exit_code) if blocked, or None if clean.
    """
    tool_input = data.get("tool_input", {})
    new_string = tool_input.get("new_string", "")

    for pattern, description in BLOCKED_PATTERNS:
        if re.search(pattern, new_string, re.IGNORECASE):
            msg = (
                f"Blocked: Edit contains '{description}'. "
                "User prefers: (1) direct breaking changes over backward compatibility shims, "
                "(2) fail-fast behavior over fallbacks, "
                "(3) explicit error handling over swallowing exceptions. "
                "Please use a different approach."
            )
            return msg, 2

    return None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    result = check(data)
    if result:
        msg, code = result
        print(msg, file=sys.stderr)
        sys.exit(code)


if __name__ == "__main__":
    main()
