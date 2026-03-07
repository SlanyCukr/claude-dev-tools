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
├── agents/               # Subagent definitions (3 agents)
│   ├── context7-docs.md
│   ├── web-research.md
│   └── chrome-devtools.md
├── hooks/                # Event-driven automation
│   ├── hooks.json        # Hook configuration
│   ├── block_antipatterns.py      # Antipattern detection (imported by orchestrator)
│   └── scripts/          # Python hook implementations
│       ├── pre_tool_checker.py    # PreToolUse orchestrator (antipatterns + tool redirect)
│       ├── tool_redirect.py       # Suggest better tools
│       ├── evasion_checker.py     # LLM-based evasion detection
│       └── _util.py               # Shared utilities
```

## Agent System

| Agent | Model | Purpose |
|-------|-------|---------|
| context7-docs | sonnet | Library documentation lookup |
| web-research | sonnet | Web search for docs |
| chrome-devtools | sonnet | Browser automation |

### Agent File Format

Each agent is a Markdown file with:
1. **YAML frontmatter**: name, description, model, tools, skills
2. **Core workflow**: Step-by-step process
3. **When to return early**: Scope limits and bail conditions
4. **Quality standards**: Domain-specific best practices
5. **Output format**: Markdown structure for results

## Hooks System

Hooks intercept Claude Code lifecycle events:

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse (Edit\|Bash) | pre_tool_checker.py | Consolidated: block antipatterns + suggest better tools |
| Stop | evasion_checker.py | LLM-based evasion detection |

## Semvex-MCP Dependency

This plugin requires [semvex-mcp](https://github.com/SlanyCukr/semvex-mcp) as a companion MCP server. Semvex provides:
- Qdrant vector DB for semantic code search
- vLLM embeddings for code understanding
- Call graph and import graph analysis

## Modifying Agents

When editing agent prompts in `agents/`:
- Preserve YAML frontmatter structure
- Keep markdown output format
- Update examples when changing behavior
- Test with representative tasks
