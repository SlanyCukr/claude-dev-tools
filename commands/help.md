---
description: Quick reference for all commands
---

# /help

## Commands

| Command | Purpose |
|---------|---------|
| `/feature` | Build something new |
| `/bugfix` | Fix problems (bugs, build errors, perf) |
| `/test` | Add tests (TDD or E2E) |
| `/security` | Security review or full audit |
| `/refactor` | Remove dead code |
| `/help` | This reference |

## Decision Tree

```
What do you need?

Build something new?
└─ /feature

Fix a problem?
└─ /bugfix (bugs, build errors, performance)

Add tests?
└─ /test (detects TDD vs E2E from context)

Security review?
└─ /security (depth based on scope)

Remove dead code?
└─ /refactor
```

## Examples

```
/feature Add user authentication with JWT
/feature Implement dark mode toggle

/bugfix Users report 500 on checkout
/bugfix Build failing with type errors
/bugfix API response takes 5 seconds

/test Add validation tests for email
/test E2E test for checkout flow

/security src/auth/login.ts
/security Full audit before deploy

/refactor Clean up src/legacy/
/refactor Remove unused dependencies
```

## Quick Tips

- `/feature` for new functionality
- `/bugfix` for anything broken
- `/test` figures out TDD vs E2E automatically
- `/security` with "full audit" for comprehensive review
- `/refactor` to clean up after major changes
