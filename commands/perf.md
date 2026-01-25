---
description: Performance investigation workflow - profile, diagnose, optimize, verify
---

# /perf

Performance investigation and optimization workflow.

## Workflow

```
1. codebase-explorer → Find hot paths and entry points
2. root-cause-agent → Analyze profiler data / slow queries
3. architect        → Design optimization approach
4. build-agent      → Implement optimization
5. chrome-devtools  → Verify improvement (frontend)
```

## Usage

```
/perf Dashboard loads slowly - takes 5+ seconds
/perf API endpoint /api/search times out under load
/perf Memory usage grows unbounded in long-running process
```

## What Happens

1. **Codebase Explorer** maps the code path from entry to exit
2. **Root Cause Agent** analyzes performance data:
   - Database query plans
   - Profiler output
   - Memory snapshots
   - Network waterfalls
3. **Architect** designs the optimization (caching, batching, indexing, etc.)
4. **Build Agent** implements the fix
5. **Chrome DevTools** verifies frontend improvements (if applicable)

## Providing Context

Include performance data if available:
- Slow query logs
- Profiler flamegraphs
- Response time percentiles
- Memory snapshots
- Network traces (HAR files)

## Common Optimizations

| Problem | Solution |
|---------|----------|
| Slow DB queries | Add indexes, optimize query, add caching |
| N+1 queries | Batch loading, eager loading |
| Memory leaks | Fix event listener cleanup, WeakRefs |
| Slow renders | Memoization, virtualization, code splitting |
| Large payloads | Pagination, compression, lazy loading |

## When to Use

- Slow page loads or API responses
- High memory usage
- Timeout errors under load
- User-reported sluggishness
