---
description: Clean up dead code, unused dependencies, and duplicate code. Uses knip, depcheck, and ts-prune for analysis.
---

# /refactor

Invokes the **refactor-cleaner** agent to identify and remove dead code.

## What This Command Does

1. **Dead Code Detection** - Find unused exports, files, dependencies
2. **Duplicate Elimination** - Consolidate similar code
3. **Dependency Cleanup** - Remove unused packages
4. **Safe Removal** - Verify before deleting
5. **Documentation** - Track all deletions

## When to Use

Use `/refactor` when:
- After major feature completion
- During scheduled cleanup sprints
- When bundle size is too large
- Before major version releases
- When test coverage is good (safety net)

## Analysis Tools

```bash
# Run knip for unused exports/files/dependencies
npx knip

# Check unused dependencies
npx depcheck

# Find unused TypeScript exports
npx ts-prune
```

## Safety Checklist

Before removing ANYTHING:
- [ ] Run detection tools
- [ ] Grep for all references
- [ ] Check dynamic imports
- [ ] Run all tests
- [ ] Create backup branch

## When NOT to Use

- During active feature development
- Right before production deployment
- When codebase is unstable
- Without proper test coverage

## Related

- Agent: agents/refactor-cleaner.md
