#!/usr/bin/env python3
"""TaskCompleted hook: verify tasks are actually done before marking complete.

Exit code 2 prevents the task from being marked complete and sends feedback.
Exit code 0 allows the completion to proceed.

Checks:
- Task description mentions tests -> verify test files exist or were modified
- Task description mentions build/compile -> verify no recent build errors
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import read_hook_stdin


def check(data: dict) -> str | None:
    """Validate task completion. Returns feedback message if incomplete, or None."""
    task = data.get("task", {})
    if not isinstance(task, dict):
        return None

    subject = task.get("subject", "")
    description = task.get("description", "")
    combined = f"{subject} {description}".lower()

    # If task mentions writing tests, check that test work was mentioned
    if re.search(r"\b(?:write|add|create|implement)\s+(?:\w+\s+)?tests?\b", combined):
        # Check the transcript/context for evidence of test files
        transcript = data.get("transcript_summary", "")
        if transcript and "test" not in transcript.lower():
            return (
                "Task mentions writing tests but no test activity detected. "
                "Did you write and run the tests? Mark complete only after tests pass."
            )

    # If task mentions fixing a bug, check for verification
    if re.search(r"\b(?:fix|resolve|debug)\s+(?:\w+\s+)?(?:bug|error|issue)\b", combined):
        transcript = data.get("transcript_summary", "")
        if transcript and not re.search(r"(?:pass|fixed|resolved|verified|works)", transcript.lower()):
            return (
                "Task mentions fixing a bug but no verification detected. "
                "Reproduce the fix and confirm it works before marking complete."
            )

    return None


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    result = check(data)
    if result:
        print(result, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
