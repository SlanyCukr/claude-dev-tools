---
description: New feature development workflow - architect, explore, TDD, implement, review
---

# /feature

Full feature development workflow using multiple agents in sequence.

## Workflow

```
1. architect        → Design the feature, identify components
2. codebase-explorer → Find existing patterns to follow
3. tdd-guide        → Write tests first (RED)
4. build-agent      → Implement code (GREEN)
5. code-reviewer    → Quality check
6. security-reviewer → Security audit (if handling auth/input)
```

## Usage

```
/feature Add user authentication with JWT tokens
/feature Implement shopping cart with persistent storage
/feature Add real-time notifications using WebSockets
```

## What Happens

1. **Architect** designs the approach and identifies files/components needed
2. **Codebase Explorer** finds existing patterns to follow (naming, structure)
3. **TDD Guide** writes failing tests first
4. **Build Agent** implements minimal code to pass tests
5. **Code Reviewer** checks for bugs and anti-patterns
6. **Security Reviewer** audits if feature touches auth, user input, or sensitive data

## When to Use

- Adding new functionality to existing codebase
- Features that touch multiple files/components
- Anything requiring architectural decisions

## When NOT to Use

- Simple bug fixes (use `/bugfix`)
- One-file changes (invoke agents directly)
- Pure refactoring (use `/cleanup`)
