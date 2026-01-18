#!/usr/bin/env python3
"""PreToolUse hook for bash-commands: fix commands that could produce large output."""

import json
import re
import sys

# Pattern -> replacement function
FIXERS = [
    # docker logs without --tail -> add --tail=100
    (
        r"(docker\s+(?:compose\s+)?logs)\b(?!.*--tail)(.*)$",
        lambda m: f"{m.group(1)} --tail=100{m.group(2)}",
    ),
    # grep piped to sort without head -> add | head -50
    (
        r"(grep.*\|\s*sort[^|]*)$",
        lambda m: f"{m.group(1)} | head -50" if "head" not in m.group(1) else m.group(0),
    ),
    # cat on .log files -> replace with tail -50
    (
        r"cat\s+(\S*\.log)\b",
        lambda m: f"tail -50 {m.group(1)}",
    ),
]


def fix_command(command: str) -> str | None:
    """Apply fixes to dangerous commands. Returns fixed command or None if no fix needed."""
    for pattern, fixer in FIXERS:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return re.sub(pattern, fixer, command, flags=re.IGNORECASE)
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    fixed = fix_command(command)
    if fixed and fixed != command:
        # Output JSON to modify the command
        tool_input["command"] = fixed
        result = {
            "permissionDecision": "allow",
            "updatedInput": tool_input,
        }
        print(json.dumps(result))
        sys.exit(0)

    # No fix needed, pass through
    sys.exit(0)


if __name__ == "__main__":
    main()
