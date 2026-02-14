---
description: Goal-backward planning with validation loop
---

# /plan

Goal-backward planning — derive "what must be TRUE?" from the goal, create a task plan, then validate the plan achieves the goal before execution.

## Usage

```
/plan Add user authentication with JWT
/plan Migrate from REST to GraphQL for the dashboard
/plan Implement real-time notifications
```

## Workflow

```
1. Take goal from user
2. Derive must_haves (observable truths, required artifacts, key links)
3. codebase-explorer    → Discover existing patterns and constraints
4. architect            → Design approach, break into tasks with dependencies
5. plan-verifier        → Check completeness (goal, acceptance criteria, tasks, dependencies, testing)
6. plan-challenger      → Find failure modes (race conditions, error paths, security)
7. plan-refiner         → Validate plan against project rules/conventions
8. If issues found      → Revise and re-validate (max 2 rounds)
9. Output approved plan as task list
```

## Must-Haves

The core of goal-backward planning. Ask "what must be TRUE?" not "what should we build?"

**Rules for must_haves:**

- Must be **user-observable** (not implementation details)
  - Good: "User can log in with email and password"
  - Bad: "AuthService class exists"
- Every truth maps to **artifacts** (files, functions, config)
- **Key links** track wiring between artifacts (A imports B, route calls handler, etc.)

Example for "Add JWT authentication":

```markdown
## Must Be True
1. User can register with email/password
2. User can log in and receive a token
3. Protected routes reject unauthenticated requests
4. Token expires after configured duration

## Artifacts
- auth router, auth service, user model, JWT utils, auth middleware

## Key Links
- auth router → auth service → user model
- auth middleware → JWT utils
- protected routes → auth middleware
```

## Plan Validation

After the architect produces a plan, validate through three stages:

1. **Completeness (plan-verifier)**: Required sections exist (goal, acceptance criteria, tasks, dependencies, testing), acceptance criteria map to tasks
2. **Assumptions (plan-challenger)**: Verify assumptions against codebase reality, generate failure scenarios (race conditions, error paths, security, edge cases)
3. **Project Rules (plan-refiner)**: Check coverage (every must_have has tasks), dependencies, and project-specific conventions

If validation finds gaps → revise plan (max 2 rounds), then present to user.

## Output Format

```markdown
## Plan: <goal>

### Must Be True
1. <observable truth>
2. ...

### Tasks
1. <task> — produces must_have #X
   - Files: <files to create/modify>
   - Depends on: <nothing or task numbers>
2. ...

### Validation
- Coverage: X/Y must_haves covered
- Project rules: PASS/issues found
```

Plan lives in Claude's task list. For persistence across sessions, use `/pause`.

## When to Use

- New features that span multiple files
- Architectural changes
- Migrations or refactors with many moving parts
- Any task where you want to think before coding

## When NOT to Use

- Small, obvious changes → `/quick`
- Single-file fixes → `/quick` or `/bugfix`
- You already have a clear plan → just execute it

## Context

$ARGUMENTS
