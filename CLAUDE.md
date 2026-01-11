# zai-speckit-plugin

Claude Code plugin for delegating work to specialized subagents with speckit integration.

## Version

Plugin version is defined in `.claude-plugin/plugin.json` (line 4).

## Project Structure

```
zai-speckit-plugin/
├── .claude-plugin/       # Plugin metadata
│   ├── plugin.json       # Name, version, description
│   └── marketplace.json  # Marketplace integration config
├── agents/               # Subagent definitions (10 agents)
│   ├── build-agent.md
│   ├── python-build-agent.md
│   ├── react-nextjs-agent.md
│   ├── code-reviewer.md
│   ├── root-cause-agent.md
│   ├── codebase-explorer.md
│   ├── context7-docs.md
│   ├── web-research.md
│   ├── chrome-devtools.md
│   └── bash-commands.md
├── hooks/                # Event-driven automation
│   ├── hooks.toml        # Hook configuration
│   ├── block_antipatterns.py
│   ├── speckit_subagent_context.py
│   ├── bash_output_monitor.py
│   ├── honesty_validator.py
│   └── session_start_context.py
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
| codebase-explorer | sonnet | Fast codebase search |
| context7-docs | sonnet | Library documentation lookup |
| web-research | sonnet | Web search for docs |
| chrome-devtools | sonnet | Browser automation |
| bash-commands | haiku | Git, npm, system commands |

### Agent File Format

Each agent is a Markdown file with:
1. **YAML frontmatter**: name, description, model, tools, skills
2. **Output rules**: TOON format specification
3. **Instruction hierarchy**: Priority of instructions
4. **Workflow phases**: Assess → Act pattern
5. **BAIL conditions**: When to return early
6. **Examples**: Concrete input/output demonstrations

### TOON Output Format

All agents return a single line:
```
TOON: /tmp/zai-speckit/toon/{unique-id}.toon
```

TOON file contains structured results:
```toon
status: done | partial | failed | bail
task: {description}
files[N]: file1.py,file2.py
notes: {blockers or suggestions}
```

## Hooks System

Hooks intercept Claude Code lifecycle events:

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse | block_antipatterns.py | Block backward compat, fallbacks, exception swallowing |
| UserPromptSubmit | speckit_subagent_context.py | Inject subagent guidance for speckit commands |
| PostToolUse | bash_output_monitor.py | Token efficiency reminder (>30 lines) |
| SubagentStop | honesty_validator.py | Validate "Honesty Over Completion" |
| SessionStart | session_start_context.py | Inject subagent usage reminders |

## Speckit Integration

Maps speckit commands to recommended agents:

| Command | Agents | Purpose |
|---------|--------|---------|
| speckit.specify | codebase-explorer | Understand patterns before spec |
| speckit.clarify | web-research, context7-docs | Research and docs |
| speckit.plan | codebase-explorer, web-research, context7-docs | Parallel exploration |
| speckit.implement | python-build-agent, react-nextjs-agent, build-agent | Specialized implementation |
| speckit.tasks | codebase-explorer | Task breakdown |

## Design Philosophy

1. **Delegation First**: Main session orchestrates, subagents execute
2. **Small Chunks**: ONE focused task per agent call
3. **Honesty Over Completion**: Partial work with clear reporting > fake completion
4. **Early Bail Pattern**: Return early if task unclear/too broad

## Modifying Agents

When editing agent prompts in `agents/`:
- Preserve YAML frontmatter structure
- Keep `<output_rules>` XML section
- Maintain instruction hierarchy
- Update examples when changing behavior
- Test with representative tasks

## Adding New Hooks

1. Add Python script to `hooks/`
2. Register in `hooks/hooks.toml`
3. Use appropriate event: PreToolUse, PostToolUse, UserPromptSubmit, SubagentStop, SessionStart
