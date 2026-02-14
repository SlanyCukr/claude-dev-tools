# claude-dev-tools

Claude Code plugin for delegating work to specialized subagents.

## Version

Plugin version is defined in `.claude-plugin/plugin.json` (line 4).

## Project Structure

```
claude-dev-tools/
├── .claude-plugin/       # Plugin metadata
│   ├── plugin.json       # Name, version, description
│   └── marketplace.json  # Marketplace integration config
├── agents/               # Subagent definitions (18 agents)
│   ├── build-agent.md
│   ├── python-build-agent.md
│   ├── react-nextjs-agent.md
│   ├── code-reviewer.md
│   ├── root-cause-agent.md
│   ├── codebase-explorer.md
│   ├── context7-docs.md
│   ├── web-research.md
│   ├── chrome-devtools.md
│   ├── bash-commands.md
│   ├── security-reviewer.md
│   ├── tdd-guide.md
│   ├── e2e-runner.md
│   ├── refactor-cleaner.md
│   ├── architect.md
│   ├── plan-refiner.md
│   ├── plan-verifier.md       # NEW
│   └── plan-challenger.md     # NEW
├── commands/             # Slash commands (11 total)
│   ├── quick.md          # /quick - Small task, minimal ceremony
│   ├── plan.md           # /plan - Goal-backward planning with verification
│   ├── research.md       # /research - Parallel research synthesis
│   ├── bugfix.md         # /bugfix - Fix problems (bugs, build, perf)
│   ├── debug.md          # /debug - Persistent debugging across sessions
│   ├── security.md       # /security - Security review or audit
│   ├── refactor.md       # /refactor - Dead code cleanup
│   ├── verify.md         # /verify - Check implementation meets goal
│   ├── pause.md          # /pause - Save session state + memories
│   ├── resume.md         # /resume - Continue from paused session + memories
│   └── help.md           # /help - Quick reference
├── rules/                # Always-on and conditional guidelines
│   ├── security.md       # Security best practices
│   ├── testing.md        # Testing requirements
│   ├── git-workflow.md   # Git workflow standards
│   ├── python-standards.md    # Python conventions (*.py only)
│   └── typescript-standards.md # TypeScript/JS conventions (*.ts/*.tsx/*.js/*.jsx only)
├── hooks/                # Event-driven automation
│   ├── hooks.json        # Hook configuration
│   ├── block_antipatterns.py
│   ├── lib/              # Hook utilities
│   │   └── utils.js
│   └── scripts/          # Node.js hook implementations
│       ├── file-checker.js        # Report-only linter
│       ├── tool-redirect.js       # Suggest better tools
│       ├── tdd-enforcer.js        # TDD reminder
│       ├── context-monitor.js     # Context usage tracking
│       ├── stop-guard.js          # Incomplete plan warning
│       ├── session-memory-loader.js # Auto-load memories
│       └── console-log-warning.js
├── lib/                  # Supporting libraries
│   └── toon.py           # TOON parser
├── scripts/              # Utility scripts
│   └── session-to-toon.sh
└── test/                 # Test files
    └── chrome-devtools-test.html
```

## Agent System

### Agent Types

| Agent | Model | Purpose |
|-------|-------|---------|
| build-agent | opus | General code implementation |
| python-build-agent | opus | Python with type hints, Ruff/mypy |
| react-nextjs-agent | opus | React/Next.js with TanStack Query |
| code-reviewer | opus | Code quality (80% confidence threshold) |
| root-cause-agent | opus | Failure diagnosis |
| security-reviewer | opus | OWASP Top 10, secrets, vulnerabilities |
| tdd-guide | opus | TDD workflow, 80% coverage |
| e2e-runner | opus | Playwright E2E tests |
| refactor-cleaner | opus | Dead code elimination, code simplification |
| architect | opus | System design, ADRs |
| plan-refiner | sonnet | Validate plans against project rules |
| plan-verifier | sonnet | Check plan completeness and coverage |
| plan-challenger | sonnet | Find failure modes and assumptions |
| codebase-explorer | sonnet | Fast codebase search |
| context7-docs | sonnet | Library documentation lookup |
| web-research | sonnet | Web search for docs |
| chrome-devtools | sonnet | Browser automation |
| bash-commands | sonnet | Git, npm, system commands |

### Agent File Format

Each agent is a Markdown file with:
1. **YAML frontmatter**: name, description, model, tools, skills
2. **Core workflow**: Step-by-step process
3. **When to return early**: Scope limits and bail conditions
4. **Quality standards**: Domain-specific best practices
5. **Output format**: Markdown structure for results

## Commands System

Eleven commands for common development workflows:

| Command | Purpose | Key Agents |
|---------|---------|------------|
| /quick | Small task, minimal ceremony | build-agent, code-reviewer |
| /plan | Goal-backward planning with verification | codebase-explorer, architect, plan-verifier, plan-challenger, plan-refiner |
| /research | Parallel research synthesis | codebase-explorer, web-research, context7-docs |
| /bugfix | Fix problems (bugs, build errors, perf) | root-cause → explore → tdd → build → review |
| /debug | Persistent debugging across sessions | root-cause-agent, codebase-explorer, bash-commands |
| /security | Security review or full audit | security-reviewer (+ explore → build if audit) |
| /refactor | Dead code cleanup | refactor-cleaner → explore → build → review |
| /verify | Check implementation meets its goal | codebase-explorer, bash-commands, code-reviewer |
| /pause | Save session state + memories | (main session, uses store_memory_tool) |
| /resume | Continue from paused session + memories | (main session, uses list_recent_memories_tool) |
| /help | Quick reference | - |

## Rules System

Guidelines that apply to development. Always-on rules apply globally, conditional rules activate only for matching file types:

| Rule File | Enforces | Scope |
|-----------|----------|-------|
| security.md | No hardcoded secrets, input validation, CSRF | Always |
| testing.md | 80% coverage, TDD for critical code | Always |
| git-workflow.md | Commit format, PR standards | Always |
| python-standards.md | Type hints, ruff, pytest, no bare except | `**/*.py` |
| typescript-standards.md | Strict mode, no any, explicit returns, ESLint | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` |

## Hooks System

Hooks intercept Claude Code lifecycle events:

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse (Edit) | block_antipatterns.py | Block backward compat, fallbacks |
| PreToolUse (*) | tool-redirect.js | Suggest better tool alternatives |
| PostToolUse (Edit) | file-checker.js | Report-only linter (ruff, eslint, golangci-lint) |
| PostToolUse (Edit) | tdd-enforcer.js | TDD reminder for implementation files |
| PostToolUse (Edit) | console-log-warning.js | Warn about console.log |
| PostToolUse (Write) | file-checker.js | Report-only linter |
| PostToolUse (Write) | tdd-enforcer.js | TDD reminder |
| PostToolUse (*) | context-monitor.js | Track context usage, warn at thresholds |
| Stop | stop-guard.js | Block on incomplete plan tasks |
| Stop | prompt hook | LLM-based evasion detection |
| SessionStart | session-memory-loader.js | Auto-load memories from previous sessions |

## Semvex-MCP Dependency

This plugin requires [semvex-mcp](https://github.com/SlanyCukr/semvex-mcp) as a companion MCP server. Semvex provides:
- Qdrant vector DB for semantic code search
- vLLM embeddings for code understanding
- Call graph and import graph analysis
- **Persistent memory** (store/search/list/delete/prune memories across sessions)

All agents, commands, and hooks assume semvex is installed and running. There are no fallbacks.

## Design Philosophy

1. **Delegation First**: Main session orchestrates, subagents execute
2. **Small Chunks**: ONE focused task per agent call
3. **Honesty Over Completion**: Partial work with clear reporting > fake completion
4. **Proactive Quality**: Use security-reviewer, code-reviewer, tdd-guide without being asked
5. **Test-Driven**: Write tests first, implement second

## Agent Orchestration

Use agents proactively based on triggers:

| Trigger | Agent | Why |
|---------|-------|-----|
| Complex feature request | architect | Break down implementation |
| Code just written/modified | code-reviewer | Quality check |
| Bug fix or new feature | tdd-guide | Tests first |
| Architectural decision | architect | System design |
| Security-sensitive code | security-reviewer | Vulnerability check |
| Build/type errors | root-cause-agent | Diagnosis |
| Dead code cleanup | refactor-cleaner | Safe removal |
| E2E test creation | e2e-runner | Playwright tests |

## Modifying Agents

When editing agent prompts in `agents/`:
- Preserve YAML frontmatter structure
- Keep markdown output format
- Update examples when changing behavior
- Test with representative tasks

## Skills System

Skills referenced in agent frontmatter (e.g., `backend-testing`, `react-query-patterns`)
are external skills provided by Claude Code or other plugins. They are invoked via
the `Skill` tool when the agent needs specialized knowledge.

## Adding New Hooks

1. Add script to `hooks/scripts/` (Node.js) or `hooks/` (Python)
2. Register in `hooks/hooks.json`
3. Use appropriate event: PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd, PreCompact
