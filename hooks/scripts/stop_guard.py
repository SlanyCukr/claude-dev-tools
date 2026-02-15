#!/usr/bin/env python3
"""Stop hook: check for incomplete plan tasks with escape hatch and user-input detection."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import is_waiting_for_user_input, read_hook_stdin

STATE_DIR = Path("/tmp")
ESCAPE_WINDOW_SECONDS = 60


def load_block_state(session_id: str) -> dict:
    """Load stop-guard state from temp file."""
    state_file = STATE_DIR / f"claude-stop-guard-{session_id}.json"
    try:
        return json.loads(state_file.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_block_state(session_id: str, state: dict) -> None:
    """Save stop-guard state to temp file."""
    state_file = STATE_DIR / f"claude-stop-guard-{session_id}.json"
    tmp_file = state_file.with_suffix(".tmp")
    try:
        tmp_file.write_text(json.dumps(state))
        tmp_file.rename(state_file)
    except OSError:
        pass


def find_unchecked_tasks(cwd: str) -> tuple[str, list[str]]:
    """Find unchecked tasks in plan files. Returns (plan_name, task_list)."""
    plans_dir = Path.home() / ".claude" / "plans"
    if not plans_dir.is_dir():
        return "", []

    basename = Path(cwd).name

    for plan_file in plans_dir.glob("*.md"):
        try:
            content = plan_file.read_text()
        except OSError:
            continue

        if cwd not in content and basename not in content and f"./{basename}" not in content:
            continue

        unchecked = [
            line.strip()
            for line in content.splitlines()
            if line.strip().startswith("- [ ]") or line.strip().startswith("* [ ]")
        ]

        if unchecked:
            return plan_file.name, unchecked

    return "", []


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    if data.get("stop_hook_active"):
        return 0

    session_id = data.get("session_id", "")
    transcript_path = data.get("transcript_path", "")
    cwd = data.get("cwd") or str(Path.cwd())

    # Always allow stop if Claude asked a question and is waiting for user input
    if transcript_path and is_waiting_for_user_input(transcript_path):
        return 0

    plan_name, unchecked = find_unchecked_tasks(cwd)
    if not unchecked:
        return 0

    # Check escape hatch: if user tried to stop within the last 60s, allow it
    if session_id:
        state = load_block_state(session_id)
        last_block = state.get("last_block_time")
        if last_block:
            elapsed = time.time() - last_block
            if elapsed <= ESCAPE_WINDOW_SECONDS:
                # Escape hatch — allow stop, fire notification
                try:
                    from notify import send_notification
                    send_notification("Claude — Stop Override", f"Escape hatch used ({len(unchecked)} tasks remaining)")
                except ImportError:
                    pass
                # Clear state
                save_block_state(session_id, {})
                return 0

        # Record this block attempt
        state["last_block_time"] = time.time()
        save_block_state(session_id, state)

    # Show specific tasks (up to 3)
    task_preview = unchecked[:3]
    task_lines = "\n".join(f"  {t}" for t in task_preview)
    remaining = f" (+{len(unchecked) - 3} more)" if len(unchecked) > 3 else ""

    reason = (
        f"Cannot stop: {len(unchecked)} incomplete task(s) in plan ({plan_name}):\n"
        f"{task_lines}{remaining}\n"
        f"Complete the tasks or use /pause first. "
        f"(Stop again within 60s to override)"
    )

    print(reason, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
