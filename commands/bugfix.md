---
description: Fix problems - bugs, build errors, performance issues
---

# /bugfix

Fix any kind of problem: runtime bugs, build errors, or performance issues.

## Usage

```
/bugfix Users report 500 errors on checkout
/bugfix TypeScript build failing with 15 errors
/bugfix Dashboard loads in 8 seconds, should be < 2s
/bugfix Memory usage grows unbounded in worker
```

## Workflow

```
1. root-cause-agent → Diagnose with evidence
2. codebase-explorer → Find related code
3. tdd-guide        → Write regression test
4. build-agent      → Implement fix
5. code-reviewer    → Verify quality
```

## Problem Types

| Type | Approach |
|------|----------|
| Runtime bug | Analyze logs/traces, form hypotheses |
| Build error | Parse errors, fix one at a time, verify |
| Performance | Profile, identify bottleneck, optimize |

## Providing Context

Include as much as possible:
- Error messages or stack traces
- When it started happening
- What changed recently
- Steps to reproduce
- Affected files or endpoints

For **performance issues**, also include:
- Current vs expected timing
- Profiler output if available
- Query execution plans

For **build errors**, include:
- Full error output
- Recent changes to types/deps

## What Happens

1. **Root Cause Agent** analyzes evidence and forms hypotheses with confidence levels
2. **Codebase Explorer** maps related code paths and dependencies
3. **TDD Guide** writes a failing test that reproduces the issue
4. **Build Agent** implements the fix
5. **Code Reviewer** verifies no regressions

## When to Use

- Production errors or failures
- Build/type errors blocking development
- Performance regressions
- Failing tests you don't understand
- Intermittent/flaky issues

## When NOT to Use

- You already know the fix (just use build-agent directly)
- It's a new feature (use `/plan`)
