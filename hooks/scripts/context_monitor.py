#!/usr/bin/env python3
"""PostToolUse hook: track context usage with session-scoped dedup and learn prompts."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import NC, CYAN, RED, YELLOW, read_hook_stdin

STATE_DIR = Path("/tmp")
MAX_TOKENS = 200000

THRESHOLDS = {
    40: {
        "message": "Context at 40% — good time to store key discoveries with store_memory_tool",
        "learn": True,
    },
    60: {
        "message": "Context at 60% — consider /compact if transitioning between phases",
        "learn": True,
    },
    75: {
        "message": "Context at 75% — store discoveries with store_memory_tool, then /compact",
    },
    80: {
        "message": "Context at 80% — prepare handoff: store state with store_memory_tool, consider /pause",
        "learn": True,
        "action": "handoff_once",
    },
    85: {
        "message": "Context at 85% — use /pause to save state, then compact or start new session",
        "action": "always_show",
    },
    90: {
        "message": "MANDATORY: /pause NOW before context is exhausted",
        "action": "mandatory",
    },
    95: {
        "message": "CRITICAL: /pause IMMEDIATELY — context nearly exhausted",
        "action": "critical",
    },
}

LEARN_PROMPT = (
    " Did you discover something worth capturing? "
    "If yes, call store_memory_tool now."
)


def read_last_usage(transcript_path: str) -> dict | None:
    """Read the last usage entry from the transcript JSONL."""
    try:
        content = Path(transcript_path).read_text()
        lines = content.strip().split("\n")

        for line in reversed(lines):
            try:
                entry = json.loads(line)
                msg = entry.get("message")
                if msg and msg.get("role") == "assistant" and msg.get("usage"):
                    return msg["usage"]
            except json.JSONDecodeError:
                continue
    except OSError:
        pass
    return None


def calculate_context_usage(usage: dict) -> int:
    """Calculate total context token usage."""
    return (
        (usage.get("input_tokens") or 0)
        + (usage.get("cache_creation_input_tokens") or 0)
        + (usage.get("cache_read_input_tokens") or 0)
    )


def load_state(session_id: str) -> dict:
    """Load session state from temp file."""
    state_file = STATE_DIR / f"claude-context-{session_id}.json"
    try:
        return json.loads(state_file.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(session_id: str, state: dict) -> None:
    """Save session state to temp file."""
    state_file = STATE_DIR / f"claude-context-{session_id}.json"
    tmp_file = state_file.with_suffix(".tmp")
    try:
        tmp_file.write_text(json.dumps(state))
        tmp_file.rename(state_file)
    except OSError:
        pass


def get_warning_level(usage_percent: float) -> int | None:
    """Get the highest warning threshold for the given usage percentage."""
    for threshold in sorted(THRESHOLDS.keys(), reverse=True):
        if usage_percent >= threshold:
            return threshold
    return None


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    transcript_path = data.get("transcript_path", "")
    session_id = data.get("session_id", "")

    if not transcript_path or not session_id:
        return 0

    latest_usage = read_last_usage(transcript_path)
    if not latest_usage:
        return 0

    current_context = calculate_context_usage(latest_usage)
    usage_percent = (current_context / MAX_TOKENS) * 100
    warning_level = get_warning_level(usage_percent)

    if not warning_level:
        return 0

    state = load_state(session_id)
    shown = state.get("shown_thresholds", [])
    threshold_config = THRESHOLDS[warning_level]
    action = threshold_config.get("action", "")

    # Session-scoped dedup: skip if already shown (unless always_show/mandatory/critical)
    if warning_level in shown and action not in ("always_show", "mandatory", "critical"):
        return 0

    # Throttle: < 30s since last warning (except 85%+)
    last_time = state.get("lastWarningTime")
    if last_time and warning_level < 85:
        elapsed = time.time() - last_time
        if elapsed < 30:
            return 0

    # Mark as shown
    if warning_level not in shown:
        shown.append(warning_level)
    state["shown_thresholds"] = shown
    state["lastWarningTime"] = time.time()
    state["lastWarningLevel"] = warning_level
    save_state(session_id, state)

    # Build message
    message = threshold_config["message"]
    if action in ("always_show", "mandatory", "critical"):
        message += f" ({usage_percent:.0f}%)"
    if threshold_config.get("learn"):
        message += LEARN_PROMPT

    # Output
    color = RED if warning_level >= 85 else YELLOW if warning_level >= 60 else CYAN
    print(f"{color}{message}{NC}", file=sys.stderr)

    print(
        json.dumps(
            {
                "systemMessage": message,
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": f"Context usage: {usage_percent:.1f}%",
                },
            }
        )
    )

    # Force action at 90%+
    if action in ("mandatory", "critical"):
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
