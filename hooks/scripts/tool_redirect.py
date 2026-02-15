#!/usr/bin/env python3
"""PreToolUse hook: suggest better tool alternatives for common bash commands.

Includes semantic vs literal grep detection to route to the right tool.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin

# Code syntax patterns — grep is appropriate (redirect to Grep tool)
CODE_SYNTAX = re.compile(
    r"(?:"
    r"\bdef\s|\bclass\s|\bimport\s|\bfrom\s"
    r"|\b==\b|->|=>"
    r"|\bfunction\s|\bself\."
    r"|\.get\(|\.set\(|\.add\("
    r"|\bconst\s|\blet\s|\bvar\s"
    r"|\breturn\s|\bif\s|\bfor\s|\bwhile\s"
    r"|\bstruct\s|\binterface\s|\benum\s"
    r"|::\w|#include"
    r")"
)

# Semantic/natural language patterns — semvex is more appropriate
SEMANTIC_PHRASES = re.compile(
    r"(?i)(?:"
    r"where\s+is|how\s+does|find\s+the|what\s+calls"
    r"|who\s+uses|look\s+for|search\s+for"
    r"|find\s+all|locate|implementation\s+of"
    r"|definition\s+of|handler\s+for"
    r"|related\s+to|responsible\s+for"
    r")"
)

REDIRECTS = {
    "grep": "Use the Grep tool instead of bash grep/rg.",
    "rg": "Use the Grep tool instead of bash grep/rg.",
    "find": "Use the Glob tool instead of bash find/fd.",
    "fd": "Use the Glob tool instead of bash find/fd.",
    "cat": "Use the Read tool instead.",
    "head": "Use the Read tool instead.",
    "tail": "Use the Read tool instead.",
    "sed": "Use the Edit tool instead.",
    "awk": "Use the Edit tool instead.",
    "echo": "Output text directly in your response instead of using echo.",
}

SEMVEX_MSG = (
    "This looks like a semantic search query. "
    "Use mcp__semvex__search_code_tool for natural language code search instead."
)

GREP_TOOL_MSG = (
    "Use the Grep tool instead of bash grep/rg. "
    "For semantic code search, use mcp__semvex__search_code_tool."
)


def get_primary_command(cmd: str) -> str:
    """Extract the primary command from a bash command string."""
    if not cmd:
        return ""
    first_segment = re.split(r"[|;&]", cmd)[0].strip()
    return first_segment.split()[0] if first_segment else ""


def get_grep_pattern(cmd: str) -> str:
    """Extract the search pattern from a grep/rg command."""
    # Remove the command name and common flags
    parts = cmd.split()
    for i, part in enumerate(parts):
        if part in ("grep", "rg"):
            continue
        if part.startswith("-"):
            continue
        # First non-flag argument is the pattern
        return part.strip("'\"")
    return ""


def classify_grep(cmd: str) -> str:
    """Classify a grep command as 'semantic', 'code', or 'generic'."""
    pattern = get_grep_pattern(cmd)
    if not pattern:
        return "generic"
    if SEMANTIC_PHRASES.search(pattern):
        return "semantic"
    if CODE_SYNTAX.search(pattern):
        return "code"
    return "generic"


def check(data: dict) -> tuple[str, int] | None:
    """Check if a Bash command should be redirected to a better tool.

    Returns (stderr_message, exit_code) if redirect needed, or None if clean.
    """
    if data.get("tool_name") != "Bash":
        return None

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    primary = get_primary_command(command)

    # Special handling for grep/rg: classify the pattern
    if primary in ("grep", "rg"):
        kind = classify_grep(command)
        if kind == "semantic":
            return SEMVEX_MSG, 2
        return GREP_TOOL_MSG, 2

    redirect = REDIRECTS.get(primary)
    if redirect:
        return redirect, 2

    return None


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    result = check(data)
    if result:
        msg, code = result
        print(msg, file=sys.stderr)
        return code

    return 0


if __name__ == "__main__":
    sys.exit(main())
