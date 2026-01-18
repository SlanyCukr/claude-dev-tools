#!/usr/bin/env python3
"""PreToolUse hook for bash-commands: auto-fix commands that could produce large output."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

DEBUG_LOG = Path("/tmp/bash-hook-debug.log")


def log_debug(msg: str) -> None:
    """Write debug message to log file."""
    with DEBUG_LOG.open("a") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def add_tail_to_docker_logs(command: str) -> str:
    """Add --tail=100 to docker logs if missing."""
    if not re.search(r"docker\s+(compose\s+)?logs\b", command, re.IGNORECASE):
        return command
    if re.search(r"--tail", command, re.IGNORECASE):
        return command
    # Insert --tail=100 after 'logs'
    return re.sub(
        r"(docker\s+(?:compose\s+)?logs)\b",
        r"\1 --tail=100",
        command,
        flags=re.IGNORECASE,
    )


def add_cut_to_docker_logs(command: str) -> str:
    """Add | cut -c1-500 to docker logs if missing."""
    if not re.search(r"docker\s+(compose\s+)?logs\b", command, re.IGNORECASE):
        return command
    if re.search(r"cut\s+-c", command, re.IGNORECASE):
        return command
    # Append cut at the end
    return command.rstrip() + " 2>&1 | cut -c1-500"


def add_head_to_grep_sort(command: str) -> str:
    """Add | head -50 to grep | sort if missing."""
    if not re.search(r"grep.*\|\s*sort", command, re.IGNORECASE):
        return command
    if re.search(r"\|\s*head", command, re.IGNORECASE):
        return command
    return command.rstrip() + " | head -50"


def replace_cat_log_with_tail(command: str) -> str:
    """Replace cat *.log with tail -50."""
    return re.sub(
        r"cat\s+(\S*\.log)\b",
        r"tail -50 \1",
        command,
        flags=re.IGNORECASE,
    )


FIXERS = [
    add_tail_to_docker_logs,
    add_cut_to_docker_logs,
    add_head_to_grep_sort,
    replace_cat_log_with_tail,
]


def fix_command(command: str) -> str:
    """Apply all fixes to command."""
    for fixer in FIXERS:
        command = fixer(command)
    return command


def main():
    log_debug("=== Hook invoked ===")

    try:
        raw_input = sys.stdin.read()
        log_debug(f"Raw stdin: {raw_input[:500]}")
        data = json.loads(raw_input)
    except json.JSONDecodeError as e:
        log_debug(f"JSON decode error: {e}")
        sys.exit(0)

    log_debug(f"Parsed data keys: {list(data.keys())}")

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    log_debug(f"Command: {command}")

    fixed = fix_command(command)
    log_debug(f"Fixed command: {fixed}")
    log_debug(f"Changed: {fixed != command}")

    if fixed != command:
        # Block the command - try stderr + exit 2 for blocking
        result = {
            "hookSpecificOutput": {
                "permissionDecision": "deny",
            },
            "systemMessage": f"Command blocked: output could be too large. Use this instead: {fixed}",
        }
        output = json.dumps(result)
        log_debug(f"Output (DENY to stderr): {output}")
        print(output, file=sys.stderr)  # Print to stderr for exit 2
        sys.exit(2)  # Exit 2 = blocking error, stderr fed to Claude
    else:
        log_debug("No modification needed")

    sys.exit(0)


if __name__ == "__main__":
    main()
