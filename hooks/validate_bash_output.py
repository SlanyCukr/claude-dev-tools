#!/usr/bin/env python3
"""PreToolUse hook for bash-commands: warn about commands that could produce large output."""

import json
import re
import sys

DANGEROUS_PATTERNS = [
    # docker logs without --tail
    (r"docker\s+(compose\s+)?logs\b(?!.*--tail)",
     "docker logs without --tail can produce huge output. Add --tail=100"),
    # grep piped to sort without head
    (r"grep.*\|\s*sort(?!.*head)",
     "grep | sort without head can produce unbounded output. Add | head -50"),
    # cat on .log files
    (r"cat\s+\S*\.log\b",
     "cat on log files is dangerous. Use tail -50 instead"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    for pattern, warning in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            msg = f"WARNING: {warning}"
            print(msg, file=sys.stderr)
            # Exit 2 to block, or 0 to warn only
            sys.exit(0)


if __name__ == "__main__":
    main()
