"""Shared utilities for hook scripts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

RED = "\033[0;31m"
YELLOW = "\033[0;33m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def read_hook_stdin() -> dict:
    """Read and parse JSON from stdin. Returns empty dict on error."""
    try:
        content = sys.stdin.read()
        if not content:
            return {}
        return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return {}


def find_git_root(start: Path | None = None) -> Path | None:
    """Walk up from start directory looking for .git. Returns repo root or None."""
    current = start or Path.cwd()
    current = current.resolve()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def check_file_length(path: str | Path) -> tuple[str, int] | None:
    """Check file length. Returns ("warn", N) at 300+, ("critical", N) at 500+, None under 300."""
    try:
        line_count = len(Path(path).read_text().splitlines())
    except OSError:
        return None
    if line_count >= 500:
        return ("critical", line_count)
    if line_count >= 300:
        return ("warn", line_count)
    return None


def get_edited_file_from_stdin() -> tuple[dict, str]:
    """Read hook stdin and extract file_path. Returns (data, file_path)."""
    data = read_hook_stdin()
    if not data:
        return {}, ""
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "") if isinstance(tool_input, dict) else ""
    return data, file_path


def is_waiting_for_user_input(transcript_path: str) -> bool:
    """Check if the last assistant message used AskUserQuestion tool."""
    try:
        content = Path(transcript_path).read_text()
        lines = content.strip().split("\n")

        for line in reversed(lines):
            try:
                entry = json.loads(line)
                msg = entry.get("message")
                if not msg or msg.get("role") != "assistant":
                    continue
                # Check tool_use blocks for AskUserQuestion
                msg_content = msg.get("content", [])
                if isinstance(msg_content, list):
                    for block in msg_content:
                        if (
                            isinstance(block, dict)
                            and block.get("type") == "tool_use"
                            and block.get("name") == "AskUserQuestion"
                        ):
                            return True
                return False
            except json.JSONDecodeError:
                continue
    except OSError:
        pass
    return False
