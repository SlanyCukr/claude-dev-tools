---
description: Code cleanup workflow - find dead code, verify dependencies, remove safely
---

# /cleanup

Dead code elimination and refactoring workflow.

## Workflow

```
1. refactor-cleaner → Find dead code (knip, depcheck, ts-prune)
2. codebase-explorer → Verify nothing depends on candidates
3. build-agent      → Remove dead code safely
4. code-reviewer    → Verify no regressions introduced
```

## Usage

```
/cleanup src/utils/ - remove unused exports
/cleanup Find and remove dead code across the project
/cleanup Clean up deprecated API endpoints
```

## What Happens

1. **Refactor Cleaner** runs analysis tools to find:
   - Unused exports
   - Unused dependencies
   - Dead code paths
   - Duplicate code
2. **Codebase Explorer** verifies candidates are truly unused
3. **Build Agent** removes dead code with clean deletions
4. **Code Reviewer** checks for accidental breakage

## Tools Used

- **knip** - Unused exports and dependencies (JS/TS)
- **depcheck** - Unused npm dependencies
- **ts-prune** - Unused TypeScript exports

## When to Use

- Before major refactoring
- After removing a feature
- Regular tech debt cleanup
- Preparing for dependency upgrades

## When NOT to Use

- Active development on those files
- Code that might be used dynamically (check carefully)
- Third-party code you don't control
