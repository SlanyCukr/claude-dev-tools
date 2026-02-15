#!/usr/bin/env python3
"""PreToolUse orchestrator: consolidated antipattern blocking and tool redirection.

Reads stdin once and runs both checks. Antipatterns checked first (blocking),
then tool redirects (suggestions). First check that returns non-zero wins.

Always runs both on Edit|Bash — each check handles its own tool_name filtering.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from _util import read_hook_stdin

from block_antipatterns import check as check_antipatterns
from tool_redirect import check as check_redirect


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    # Antipatterns first (hard block on Edit)
    result = check_antipatterns(data)
    if result:
        msg, code = result
        print(msg, file=sys.stderr)
        return code

    # Tool redirects (suggestions on Bash)
    result = check_redirect(data)
    if result:
        msg, code = result
        print(msg, file=sys.stderr)
        return code

    return 0


if __name__ == "__main__":
    sys.exit(main())
