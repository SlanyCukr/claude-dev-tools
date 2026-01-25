---
description: Incrementally fix TypeScript and build errors. Parses error output, explains issues, applies fixes one at a time.
---

# /build-fix

Invokes the **root-cause-agent** agent to diagnose and fix build errors.

## What This Command Does

1. **Run Build** - Execute `npm run build` or `pnpm build`
2. **Parse Errors** - Group by file, sort by severity
3. **For Each Error**:
   - Show error context (5 lines before/after)
   - Explain the issue
   - Propose fix
   - Apply fix
   - Re-run build
   - Verify error resolved
4. **Stop If**:
   - Fix introduces new errors
   - Same error persists after 3 attempts
   - User requests pause
5. **Show Summary** - Errors fixed, remaining, new

## When to Use

Use `/build-fix` when:
- Build is failing with TypeScript errors
- After major refactoring
- After dependency updates
- When type definitions changed
- After merge conflicts in types

## Workflow

```
Run build → Parse errors → Fix one → Verify → Repeat
```

**Important**: Fix one error at a time for safety.

## Stop Conditions

The agent will stop if:
- A fix introduces new errors
- The same error persists after 3 attempts
- All errors are fixed

## Related

- Agent: agents/root-cause-agent.md
