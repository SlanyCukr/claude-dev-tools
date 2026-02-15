#!/usr/bin/env python3
"""SessionStart hook: instruct Claude to load memories on session start."""

from __future__ import annotations

import json
import sys


def main() -> int:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": (
                        "IMPORTANT: Before doing anything else, call "
                        "list_recent_memories_tool(hours_back=48) to load context "
                        "from previous sessions. Review the memories and use them "
                        "to inform your work."
                    ),
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
