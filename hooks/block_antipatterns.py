#!/usr/bin/env python3
"""PreToolUse hook: block edits containing anti-patterns like backward compatibility or fallbacks."""

import json
import re
import sys

BLOCKED_PATTERNS = [
    (r"backwards?\s+compatibility", "backward compatibility"),
    (r"\bfallback\b", "fallback"),
    (r"except\s*:\s*pass", "bare except with pass (exception swallowing)"),
    (r"except\s+Exception\s*:\s*pass", "except Exception with pass (exception swallowing)"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

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
            print(msg, file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
