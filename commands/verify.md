---
description: Check if implementation meets its goal
---

# /verify

Goal-backward verification — derive "what must be TRUE for this to be complete?" and check each criterion with evidence.

## Usage

```
/verify The checkout flow handles all payment methods
/verify                    (derives goal from .handoff.md, .debug-session.md, or recent commits)
/verify done with the auth refactor
```

## Goal Sources

If no explicit goal is provided, derive from (in priority order):

1. `.handoff.md` — "What Was Being Done" section
2. `.debug-session.md` — "Problem" section
3. Recent git commits — infer goal from commit messages

If none found, ask the user to state the goal.

## Verification Levels

Check each artifact at 4 levels — don't stop at "it exists":

| Level | Question | Example Check |
|-------|----------|---------------|
| **Exists** | Does the artifact exist? | File present, function defined |
| **Substantive** | Is it real code, not a stub? | No TODO, no `return null`, no empty handlers, no console.log-only |
| **Wired** | Is it imported AND actually used? | Not just imported — called from the right places |
| **Functional** | Does it work? | Tests pass, build succeeds, manual verification |

## Stub Detection Patterns

Flag these as incomplete:

- `TODO`, `FIXME`, `HACK` comments
- `return null`, `return []`, `return {}` without logic
- Empty function/method bodies
- `console.log`-only implementations
- `pass` or `...` in Python
- `throw new Error('not implemented')`

## Workflow

```
1. Derive must-be-true criteria from the goal
2. codebase-explorer → Check each criterion (exists, substantive, wired)
3. bash-commands     → Run tests, build, lint (functional check)
4. code-reviewer     → Spot-check quality of implementation
5. Output pass/fail checklist with evidence
```

**Key rule**: Do NOT trust claims — verify what actually exists in the codebase.

## Output Format

```markdown
## Verification: <goal>

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | <what must be true> | PASS/FAIL | <specific evidence> |
| 2 | ... | ... | ... |

## Summary
X/Y criteria passed.

## Recommended Actions (if failures)
- <specific action to fix each failure>
```

## When to Use

- After completing a feature or fix
- After `/debug done` to verify the fix
- Before marking a task as done
- Before committing a significant change
- Code review sanity check

## When NOT to Use

- Mid-implementation (finish first, then verify)
- For security-specific checks → `/security`

## Context

$ARGUMENTS
