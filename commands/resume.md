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
4. **Load recent memories** via `list_recent_memories_tool(hours_back=48)` filtered by project
5. **Merge handoff + memories into context**
6. **Report the full context including relevant memories**
7. Check for active `.debug-session.md` → report if found
8. Run `git status` → report uncommitted changes
9. Delete `.handoff.md` after successfully loading context
10. Continue with the next steps from the handoff

### Memory Integration

The resume command integrates with the semvex memory system to restore context from previous sessions. This requires semvex memory tools to be available.

**What gets loaded:**
- **Recent memories**: All memories from the last 48 hours related to this project
- **Cross-session context**: Discoveries and decisions from previous sessions
- **File-specific memories**: Insights associated with specific files

**Why memory matters:**
- Handoff files only capture the most recent session
- Memories provide continuity across multiple pause/resume cycles
- Memories can surface relevant context from different parts of the codebase
- Memories help avoid repeating past discoveries

**Example merged context:**
```markdown
Handoff: Working on auth refactor - completed JWT validation, in progress on refresh token rotation.

Related memories from past 48h:
- "src/auth/jwt.js:42 - Need to handle expired tokens gracefully during refresh flow" (2 hours ago)
- "Discovered: Refresh token rotation requires Redis store for blacklist" (yesterday)
- "Decision: Use sliding window expiration for tokens" (1 day ago)
```

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
