---
description: Persistent debugging across sessions
---

# /debug

Persistent debugging with state that survives context resets. Wraps `root-cause-agent` with a `.debug-session.md` state file.

## Usage

```
/debug Users see 500 errors on checkout after last deploy
/debug                          (continue existing session)
/debug done                     (close session, suggest /verify)
```

## Modes

| Mode | Trigger | Action |
|------|---------|--------|
| New session | `/debug <problem>` | Create `.debug-session.md`, start investigation |
| Continue | `/debug` (file exists) | Read state, resume from where we left off |
| Close | `/debug done` | Write conclusion, suggest `/verify` |

## State File: `.debug-session.md`

Created in project root. Structure:

```markdown
# Debug Session

## Problem (immutable after creation)
<problem description>

## Hypotheses
- [ ] TESTING: <hypothesis> — <what we're checking>
- [x] CONFIRMED: <hypothesis> — <evidence>
- [~] REJECTED: <hypothesis> — <evidence>

## Evidence Log (append-only, chronological)
- [timestamp] <observation or finding>

## Dead Ends (DO NOT re-investigate)
- <approach> — <why it failed>

## Conclusion
<resolution when /debug done>
```

**Key rule**: Update the file BEFORE taking any investigative action. If context resets mid-investigation, the file preserves all progress.

## Investigation Techniques

Use these systematically — don't just read code and guess:

| Technique | When to Use |
|-----------|-------------|
| **Binary search** | Narrow down which commit/change introduced the bug |
| **Minimal reproduction** | Create smallest case that triggers the issue |
| **Git bisect** | Find exact commit that broke things |
| **Differential debugging** | Compare working vs broken state |
| **Comment out everything** | Strip to minimum, add back until it breaks |

## Workflow

```
1. Read .debug-session.md   → Load accumulated context (if continuing)
2. root-cause-agent         → Investigate with "do NOT re-investigate dead ends"
3. codebase-explorer        → Trace code paths, find related code
4. bash-commands             → Run tests, check logs, reproduce
5. Update .debug-session.md → Record findings before next action
6. Repeat 2-5 until resolved
```

## Hypothesis Rules

Every hypothesis must be **falsifiable** — state what evidence would CONFIRM and what would REJECT it:

```markdown
- [ ] TESTING: Memory leak in WebSocket handler
  - CONFIRM IF: heap grows steadily with active connections
  - REJECT IF: heap is stable regardless of connection count
```

## When to Use

- Bug persists across multiple investigation sessions
- Complex issue requiring systematic elimination
- Need to hand off debugging to another session
- Issue involves multiple interacting systems

## When NOT to Use

- Simple bugs with obvious cause → `/bugfix`
- Build errors → `/bugfix`
- Performance issues with clear bottleneck → `/bugfix`

## Context

$ARGUMENTS
