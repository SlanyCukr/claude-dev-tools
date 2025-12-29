# dev-workflow

A Claude Code plugin providing specialized agents, commands, skills, and hooks for efficient coding sessions.

## Installation

### Option 1: Using the plugin directory flag (for testing)
```bash
claude --plugin-dir /path/to/dev-workflow-plugin
```

### Option 2: Add to settings.json
```json
{
  "enabledPlugins": {
    "dev-workflow@dev-workflow-local": true
  },
  "extraKnownMarketplaces": {
    "dev-workflow-local": {
      "source": {
        "source": "github",
        "repo": "slanycukr/dev-workflow"
      }
    }
  }
}
```

## Components

### Agents

| Agent | Description | Model |
|-------|-------------|-------|
| `build-agent` | Implements code changes with focused task execution | opus |
| `code-reviewer` | Reviews code for bugs/quality (>=80% confidence threshold) | opus |
| `root-cause-agent` | Diagnoses failures with systematic evidence gathering | opus |
| `codebase-explorer` | Fast codebase search and exploration | sonnet |
| `context7-docs` | Library documentation lookup via Context7 | sonnet |
| `web-research` | Web search for docs and best practices | sonnet |
| `chrome-devtools` | Browser automation via Chrome DevTools | sonnet |

### Commands

| Command | Description |
|---------|-------------|
| `/dev-workflow:analyze-session <session-id>` | Analyze session transcripts to suggest skill/workflow improvements |
| `/dev-workflow:feature-dev <description>` | Context-efficient feature development workflow |

### Skills

| Skill | Description |
|-------|-------------|
| `jira` | Interact with Jira issues using jira-cli with token-efficient output |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| Speckit Subagent Context | UserPromptSubmit | Injects subagent guidance for speckit commands |
| Bash Output Monitor | PostToolUse | Token efficiency reminder when Bash output exceeds 30 lines |
| Honesty Validator | SubagentStop | Validates subagent work follows "Honesty Over Completion" principle |
| Session Context | SessionStart | Injects subagent usage reminders |

## Philosophy

This plugin implements the **Subagent Usage Philosophy**:

- **Context Preservation**: Main session orchestrates, subagents execute heavy work
- **Small Chunks**: Each subagent gets ONE focused task
- **Honesty Over Completion**: Partial work with clear reporting is success; silent gaps are failure
- **Early Bail Pattern**: Subagents return early if task is unclear, too broad, or confidence is low

## License

MIT
