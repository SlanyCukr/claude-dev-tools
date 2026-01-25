---
description: Dead code cleanup - find, verify, and safely remove unused code
---

# /refactor

Find and remove dead code, unused dependencies, and duplicates.

## Usage

```
/refactor src/utils/ - clean up unused exports
/refactor Find dead code across the project
/refactor Remove deprecated API endpoints
/refactor Clean up after removing the legacy auth system
```

## Workflow

```
1. refactor-cleaner → Find dead code (knip, depcheck, ts-prune)
2. codebase-explorer → Verify nothing depends on candidates
3. build-agent      → Remove dead code safely
4. code-reviewer    → Verify no regressions
```

## What Gets Found

- Unused exports
- Unused files
- Unused dependencies (npm packages)
- Duplicate/similar code
- Dead code paths
- Commented-out code

## Analysis Tools

```bash
# Unused exports, files, dependencies
npx knip

# Unused npm dependencies
npx depcheck

# Unused TypeScript exports
npx ts-prune
```

## Safety Process

1. **Detect** - Run analysis tools
2. **Verify** - Grep for dynamic references
3. **Test** - Ensure tests pass
4. **Remove** - Clean deletion (no commenting out)
5. **Log** - Document what was removed

## When to Use

- After completing a major feature
- During cleanup sprints
- When bundle size is too large
- Before major version releases
- When test coverage provides safety net

## When NOT to Use

- During active feature development
- Right before production deployment
- When codebase is unstable
- Without proper test coverage (risky)

## Related

- Agent: agents/refactor-cleaner.md
