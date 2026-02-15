---
description: Quick reference for all commands
---

# /help

## Commands

| Command | Purpose |
|---------|---------|
| `/quick` | Execute a small task with minimal ceremony |
| `/plan` | Goal-backward planning with validation loop |
| `/research` | Parallel research synthesis |
| `/bugfix` | Fix problems (bugs, build errors, perf) |
| `/debug` | Persistent debugging across sessions |
| `/review` | Code quality + security review |
| `/security` | Security review or full audit |
| `/refactor` | Remove dead code |
| `/verify` | Check if implementation meets its goal |
| `/pause` | Save session state for later |
| `/resume` | Continue from a paused session |
| `/help` | This reference |

## Decision Tree

```
Small, well-defined task?          -> /quick
  (< 3 files, clear instructions, no ambiguity)
Need to plan something?            -> /plan
  (multi-step, architectural decisions, unclear scope)
Need to research before deciding?  -> /research
  (comparing libraries, patterns, or approaches)
Fix a problem?
|-- You know the cause or file     -> /bugfix
|     (error message points to it, single root cause)
+-- Cause unclear or spans sessions -> /debug
      (intermittent, hard to reproduce, needs investigation)
Review code after changes?         -> /review
  (quality + security in one pass)
Deep security audit?               -> /security
  (pre-deploy, auth changes, OWASP compliance)
Remove dead code?                  -> /refactor
Check if work is complete?         -> /verify
Stopping for now?                  -> /pause
Coming back?                       -> /resume
```

## Examples

```
/quick Fix the typo in the error message
/quick Add created_at index to orders table

/plan Add user authentication with JWT
/plan Migrate from REST to GraphQL

/research Best approach for real-time updates
/research State management options for dashboard

/bugfix Users report 500 on checkout
/bugfix Build failing with type errors

/debug Users see 500 errors after last deploy
/debug              (continue existing session)
/debug done         (close session)

/review src/services/     (review recent changes in directory)
/review git diff          (review uncommitted changes)

/security src/auth/login.ts
/security Full audit before deploy

/refactor Clean up src/utils/
/refactor Remove unused dependencies

/verify The checkout flow handles all payment methods
/verify              (derives goal from context)

/pause
/resume
```

## Cross-Feature Interactions

```
/research -- standalone, feeds into /plan
/plan     -- standalone, can follow up with /verify
/quick    -- standalone, can follow up with /verify
/review   -- standalone, runs after implementation
/debug    -- creates .debug-session.md
              |-- /pause references it
              |-- /resume reports it
              +-- /debug done -> suggest /verify
/pause    -- creates .handoff.md (references .debug-session.md)
              +-- /resume reads and deletes .handoff.md
/verify   -- reads .handoff.md or .debug-session.md as goal sources
```
