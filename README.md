# zai-speckit-plugin

A Claude Code plugin for delegating work to **Z.AI GLM-4.7** powered subagents, with **speckit** integration.

## Overview

This plugin implements a delegation-first workflow where Claude orchestrates while subagents (routed to Z.AI's GLM-4.7 via a proxy) execute the actual work. The agents are specifically prompted to work well with GLM-4.7's capabilities.

### How It Works

1. **Claude as Orchestrator**: The main Claude session plans and coordinates
2. **Proxy Routing**: A separate proxy intercepts subagent requests and routes them to Z.AI
3. **GLM-4.7 Execution**: Subagents run on GLM-4.7 for cost-effective, high-quality execution
4. **Speckit Integration**: Hooks automatically inject subagent recommendations for speckit commands

## Installation

### Add to settings.json
```json
{
  "enabledPlugins": {
    "zai-speckit-plugin@zai-speckit": true
  },
  "extraKnownMarketplaces": {
    "zai-speckit": {
      "source": {
        "source": "github",
        "repo": "SlanyCukr/zai-speckit-plugin"
      }
    }
  }
}
```

## Components

### Agents (15 Total)

| Agent | Purpose | Model |
|-------|---------|-------|
| `build-agent` | General code implementation | opus |
| `python-build-agent` | Python with type hints, Ruff/mypy | opus |
| `react-nextjs-agent` | React/Next.js with TanStack Query | opus |
| `code-reviewer` | Code quality (80% confidence threshold) | opus |
| `root-cause-agent` | Failure diagnosis | opus |
| `security-reviewer` | OWASP Top 10, secrets, vulnerabilities | opus |
| `tdd-guide` | TDD workflow, 80% coverage | opus |
| `e2e-runner` | Playwright E2E tests | opus |
| `refactor-cleaner` | Dead code elimination | opus |
| `architect` | System design, ADRs | opus |
| `codebase-explorer` | Fast codebase search | sonnet |
| `context7-docs` | Library documentation lookup | sonnet |
| `web-research` | Web search for docs | sonnet |
| `chrome-devtools` | Browser automation | sonnet |
| `bash-commands` | Git, npm, system commands | sonnet |

### Commands

#### Workflow Commands (Multi-Agent)

| Command | Workflow | Purpose |
|---------|----------|---------|
| `/feature` | architect → explore → tdd → build → review | New feature development |
| `/bugfix` | root-cause → explore → tdd → build → review | Bug investigation and fix |
| `/cleanup` | refactor → explore → build → review | Dead code removal |
| `/perf` | explore → root-cause → architect → build | Performance optimization |
| `/integrate` | docs → research → architect → build → tdd | Library integration |
| `/audit` | security → explore → build → security | Full security audit |

#### Single-Agent Commands

| Command | Agent | Purpose |
|---------|-------|---------|
| `/tdd` | tdd-guide | Test-driven development |
| `/e2e` | e2e-runner | Playwright test generation |
| `/security` | security-reviewer | Quick security review |
| `/refactor` | refactor-cleaner | Dead code analysis |
| `/build-fix` | root-cause-agent | Build error resolution |

### Hooks

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse (Edit) | block_antipatterns.py | Block backward compat, fallbacks |
| PreToolUse (Bash) | validate_bash_output.py | Validate bash command safety |
| PreToolUse (*) | suggest-compact.js | Suggest compaction after many tool calls |
| PostToolUse (Edit) | console-log-warning.js | Warn about console.log |
| SessionStart | session-start.js | Load previous context |
| SessionEnd | session-end.js | Persist session state |
| PreCompact | pre-compact.js | Save state before compaction |

## Workflows

### 1. New Feature Development

Best for: Adding new functionality to an existing codebase.

```
1. architect        → Design the feature, identify components
2. codebase-explorer → Find existing patterns to follow
3. tdd-guide        → Write tests first (RED)
4. python-build-agent / react-nextjs-agent → Implement (GREEN)
5. code-reviewer    → Quality check
6. security-reviewer → Security audit (if auth/input handling)
```

**Example prompt:**
> "Add user authentication with JWT tokens"

### 2. Bug Investigation & Fix

Best for: Debugging production issues or failing tests.

```
1. root-cause-agent → Diagnose with logs/traces
2. codebase-explorer → Find related code
3. tdd-guide        → Write regression test first
4. build-agent      → Fix the bug
5. code-reviewer    → Verify fix quality
```

**Example prompt:**
> "Users report 500 errors on checkout - investigate and fix"

### 3. Code Cleanup & Refactoring

Best for: Technical debt reduction, removing dead code.

```
1. refactor-cleaner → Find dead code (knip, depcheck)
2. codebase-explorer → Verify nothing depends on it
3. build-agent      → Remove dead code
4. code-reviewer    → Verify no regressions
```

**Example prompt:**
> "Clean up unused exports and dead code in src/utils/"

### 4. Security Hardening

Best for: Pre-deployment security review, handling sensitive data.

```
1. security-reviewer → Full OWASP audit
2. codebase-explorer → Find all input entry points
3. build-agent      → Fix vulnerabilities
4. security-reviewer → Verify fixes
```

**Example prompt:**
> "Review authentication flow for security issues"

### 5. Adding E2E Tests

Best for: Critical user flows, regression prevention.

```
1. codebase-explorer → Understand the flow
2. e2e-runner       → Generate Playwright tests
3. bash-commands    → Run tests
4. e2e-runner       → Fix flaky tests if any
```

**Example prompt:**
> "Add E2E tests for the checkout flow"

### 6. Library Integration

Best for: Adding new dependencies, learning APIs.

```
1. context7-docs    → Get library documentation
2. web-research     → Find best practices/examples
3. architect        → Design integration approach
4. build-agent      → Implement integration
5. tdd-guide        → Add tests
```

**Example prompt:**
> "Integrate Stripe for payment processing"

### 7. Performance Investigation

Best for: Slow queries, memory leaks, bottlenecks.

```
1. codebase-explorer → Find hot paths
2. root-cause-agent → Analyze with profiler data
3. architect        → Design optimization
4. build-agent      → Implement fix
5. chrome-devtools  → Verify in browser (frontend)
```

**Example prompt:**
> "Dashboard loads slowly - investigate and optimize"

### 8. Quick Fixes (Single Agent)

For simple, well-defined tasks, use one agent directly:

| Task | Agent |
|------|-------|
| "Run the tests" | bash-commands |
| "What does UserService do?" | codebase-explorer |
| "Check Prisma docs for transactions" | context7-docs |
| "Review this PR for issues" | code-reviewer |
| "Is this SQL injection safe?" | security-reviewer |

## Parallel Execution

Run independent agents simultaneously for speed:

```
# Good: These don't depend on each other
├── codebase-explorer → Find auth patterns
├── context7-docs     → Get JWT library docs
└── web-research      → Find security best practices

# Then: Use results together
└── architect         → Design with all context
```

## Speckit Integration

When you use speckit commands, the plugin automatically injects guidance:

- `speckit.specify` → Recommends `codebase-explorer` for pattern discovery
- `speckit.clarify` → Recommends `web-research` and `context7-docs`
- `speckit.plan` → Recommends parallel exploration with multiple subagents
- `speckit.implement` → Recommends `python-build-agent` or `react-nextjs-agent`
- `speckit.tasks` → Recommends `codebase-explorer` for file structure understanding

## Philosophy

### Delegation First
- **Main session context is precious** - every token counts
- **Subagents run in isolation** - their token usage doesn't pollute main context
- **Parallelization** - run 2-3 subagents simultaneously for efficiency

### Small Chunks Only
Give each subagent ONE focused task. Large chunks lead to:
- Lazy implementations
- Quality degradation
- Silently skipped steps

### Honesty Over Completion
- Not completing work is NOT an error
- The only error is claiming "done" when steps were skipped
- Partial work with clear reporting is SUCCESS

### Early Bail Pattern
Subagents should return early (without doing work) if:
- Task is unclear → ask for clarification
- Task is too broad → suggest how to split
- Confidence is low → explain concerns

## Related Projects

- **Proxy**: Separate repository that intercepts Claude Code requests and routes subagent calls to Z.AI
- **Speckit**: GitHub-based specification workflow that pairs with this plugin

## License

MIT
