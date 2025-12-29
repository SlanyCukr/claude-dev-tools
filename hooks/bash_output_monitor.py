#!/usr/bin/env python3
"""PostToolUse hook: nudge token efficiency when Bash output exceeds threshold."""

import json
import sys

THRESHOLD = 30

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        return

    # Claude Code provides tool_response object with stdout/stderr
    tool_response = data.get("tool_response", {})
    if isinstance(tool_response, dict):
        output = tool_response.get("stdout", "")
    else:
        output = str(tool_response)
    line_count = len(output.splitlines())

    if line_count > THRESHOLD:
        msg = (f"Token efficiency reminder: Bash returned {line_count} lines (>{THRESHOLD}). "
               "Consider: (1) pipe to head/tail/grep, (2) use --quiet/--silent flags, "
               "(3) redirect verbose output to /dev/null, (4) run in background with run_in_background=true.")
        # Exit code 2 + stderr shows message to Claude
        print(msg, file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
