---
description: Bug investigation and fix workflow - diagnose, test, fix, review
---

# /bugfix

Systematic bug investigation and fix using evidence-based diagnosis.

## Workflow

```
1. root-cause-agent → Diagnose with logs/traces/code
2. codebase-explorer → Find related code and dependencies
3. tdd-guide        → Write regression test first
4. build-agent      → Fix the bug
5. code-reviewer    → Verify fix quality
```

## Usage

```
/bugfix Users report 500 errors on checkout
/bugfix Login fails intermittently with timeout
/bugfix Memory usage grows over time in worker process
```

## What Happens

1. **Root Cause Agent** analyzes evidence (logs, traces, git history) and forms hypotheses
2. **Codebase Explorer** finds related code paths and dependencies
3. **TDD Guide** writes a failing test that reproduces the bug
4. **Build Agent** implements the fix
5. **Code Reviewer** verifies the fix doesn't introduce new issues

## Providing Context

Include as much context as possible:
- Error messages or stack traces
- When it started happening
- What changed recently (deploys, config changes)
- Steps to reproduce
- Affected files or endpoints

## When to Use

- Production errors or failures
- Failing tests you don't understand
- Intermittent/flaky issues
- Performance regressions

## When NOT to Use

- You already know the fix (just use build-agent)
- It's a new feature, not a bug (use `/feature`)
