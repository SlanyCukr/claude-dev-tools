---
description: Execute a small task with minimal ceremony
---

# /quick

Minimal-ceremony task execution. No planning pipeline, no spec — just do the thing and commit.

## Usage

```
/quick Add a loading spinner to the dashboard
/quick Fix the typo in the error message
/quick Rename UserDTO to UserResponse
/quick Add created_at index to orders table
```

## Workflow

```
1. Assess scope     → Bail if too large (suggest /plan instead)
2. codebase-explorer → Understand area (only if unfamiliar)
3. build-agent      → Implement the change
4. code-reviewer    → Quick review (only if >10 lines changed)
5. Commit           → One atomic commit, conventional format
```

## Scope Guard

Before starting, evaluate the task. **Bail and suggest alternatives** if:

- Task spans multiple features or domains → suggest `/plan`
- Estimated change exceeds ~100 lines → suggest `/plan`
- Requirements are unclear or ambiguous → ask for clarification
- Task requires architectural decisions → suggest `/plan`

The point of `/quick` is speed through simplicity. If the task isn't simple, use the right tool.

## Commit Convention

One task = one commit. Use conventional commit format:

```
feat: add loading spinner to dashboard
fix: correct typo in checkout error message
refactor: rename UserDTO to UserResponse
```

No state files. The git commit IS the breadcrumb.

## When to Use

- Small, well-defined changes
- Single-file or few-file edits
- Bug fixes where you already know the cause
- Renames, typo fixes, small refactors
- Adding a single function or component

## When NOT to Use

- Multi-feature changes → `/plan`
- Unclear requirements → clarify first
- Debugging unknown issues → `/debug` or `/bugfix`
- Changes requiring research → `/research` then `/plan`

## Context

$ARGUMENTS
