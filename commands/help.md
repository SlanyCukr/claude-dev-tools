---
description: Quick reference for all available commands
---

# /help

## Quick Reference

**What do you want to do?**

### Build Something New
```
/feature <description>     Full workflow: design → test → build → review
/integrate <library>       Add a new library or service
```

### Fix Something Broken
```
/bugfix <problem>          Investigate and fix with regression test
/build-fix                 Fix TypeScript/build errors one by one
```

### Improve Code Quality
```
/cleanup [path]            Find and remove dead code
/refactor                  Analyze dead code (no removal)
/security <file/scope>     Quick security review
/audit <scope>             Full security audit with fixes
```

### Add Tests
```
/tdd <feature>             Write tests first, then implement
/e2e <flow>                Generate Playwright E2E tests
```

### Investigate Performance
```
/perf <problem>            Profile, diagnose, optimize
```

## Decision Tree

```
Is it a new feature?
├─ Yes → /feature
└─ No
   Is something broken?
   ├─ Build errors → /build-fix
   ├─ Runtime bug → /bugfix
   └─ No
      Is it about quality?
      ├─ Dead code → /cleanup
      ├─ Security → /audit or /security
      ├─ Need tests → /tdd or /e2e
      └─ Performance → /perf
```

## Command Complexity

| Simple (1 agent) | Workflow (multi-agent) |
|------------------|------------------------|
| /security | /audit |
| /refactor | /cleanup |
| /tdd | /feature |
| /e2e | /bugfix |
| /build-fix | /perf |
| | /integrate |

## Examples

```
/feature Add dark mode toggle to settings
/bugfix API returns 500 when user has no profile
/cleanup src/legacy/ - remove deprecated helpers
/integrate Sentry for error tracking
/perf Homepage takes 8 seconds to load
/audit Check payment flow before launch
/tdd Add validation for email field
/e2e Test the complete checkout flow
```
