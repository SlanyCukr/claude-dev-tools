---
description: Save session state for later
---

# /pause

Save current session state to a handoff file for resuming later. The main session introspects its own context and writes the state — no subagents (they wouldn't have the context).

## Usage

```
/pause
/pause Stopping for lunch, was working on the auth refactor
```

## State File: `.handoff.md`

Created in project root:

```markdown
# Session Handoff

## What Was Being Done
<current task/goal description>

## Completed
- <item 1>
- <item 2>

## In Progress
- <item with current state>

## Next Steps
- <what to do next, in priority order>

## Key Files Modified
- <file path> — <what changed>

## Open Questions
- <unresolved decisions or uncertainties>

## Git State
- Branch: <branch name>
- Uncommitted changes: <yes/no, summary if yes>

## Active Debug Session
<references .debug-session.md if one exists, otherwise "None">
```

## Workflow

This command does NOT delegate to subagents. The main session:

1. Introspects current context (what was being done, what's done, what's next)
2. Checks `git status` and `git branch`
3. Checks for active `.debug-session.md`
4. Writes `.handoff.md` to project root
5. **Store session summary as memory** via `store_memory_tool(content=<summary>, context="session_pause", type="session_summary", tags=["session", "handoff"], session_id=<current_session>)`
6. **Store key discoveries as individual memories** via `store_memory_tool(content=<discovery>, context=<relevant_file_or_context>, type="discovery", tags=[<relevant_tags>], session_id=<current_session>)`
7. Suggests clearing context for a fresh start on resume

### Memory Integration

The pause command integrates with the semvex memory system to provide cross-session continuity beyond the handoff file. This requires semvex memory tools to be available.

**What gets stored:**
- **Session summary**: A condensed version of `.handoff.md` with the core context
- **Key discoveries**: Important findings, insights, or decisions made during the session

**Why memory matters:**
- Handoff files are single-session (deleted after resume)
- Memories persist across multiple sessions and can be queried later
- Memories can be associated with specific files or contexts
- Memories provide better searchability for future work

**Example memory storage:**
```markdown
Session summary stored: "Working on auth refactor - completed JWT validation, in progress on refresh token rotation. Next: implement token revocation."
Discovery stored: "src/auth/jwt.js:42 - Need to handle expired tokens gracefully during refresh flow"
```

## When to Use

- Stopping work for the day
- Switching to a different task
- Context getting too large, need a fresh session
- Handing off to someone else

## When NOT to Use

- Work is complete (just commit instead)
- Nothing meaningful to preserve

## Context

$ARGUMENTS
