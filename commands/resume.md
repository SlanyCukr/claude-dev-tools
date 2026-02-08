---
description: Continue from a paused session
---

# /resume

Read the handoff file and restore context from a previous session. Counterpart to `/pause`.

## Usage

```
/resume
```

## Workflow

This command does NOT delegate to subagents. The main session:

1. Read `.handoff.md` from project root
2. If not found → report "No handoff file found. Nothing to resume."
3. Check staleness — warn if file is >1 week old (based on file modification time)
4. Report the full context: what was being done, completed items, next steps
5. Check for active `.debug-session.md` → report if found
6. Run `git status` → report uncommitted changes
7. Delete `.handoff.md` after successfully loading context
8. Continue with the next steps from the handoff

## Staleness Warning

If `.handoff.md` is older than 1 week:

```
Warning: Handoff file is X days old. The codebase may have changed
significantly. Verify next steps are still relevant before proceeding.
```

## When to Use

- Starting a new session after `/pause`
- Picking up where you or someone else left off

## When NOT to Use

- No previous `/pause` was done
- Starting fresh on a new task

## Context

$ARGUMENTS
