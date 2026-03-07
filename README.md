# claude-dev-tools

A Claude Code plugin for delegating work to specialized subagents.

## Overview

This plugin implements a delegation-first workflow where Claude orchestrates while subagents execute the actual work.

## Installation

### Add to settings.json
```json
{
  "enabledPlugins": {
    "claude-dev-tools@claude-dev-tools": true
  },
  "extraKnownMarketplaces": {
    "claude-dev-tools": {
      "source": {
        "source": "github",
        "repo": "SlanyCukr/claude-dev-tools"
      }
    }
  }
}
```

## Components

### Agents (3 Total)

| Agent | Purpose | Model |
|-------|---------|-------|
| `context7-docs` | Library documentation lookup | sonnet |
| `web-research` | Web search for docs/best practices | sonnet |
| `chrome-devtools` | Browser automation | sonnet |

### Hooks

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse (Edit\|Bash) | pre_tool_checker.py | Block antipatterns + suggest better tools |
| Stop | evasion_checker.py | LLM-based evasion detection |

#### Antipattern Blocking (PreToolUse)

Blocks edits containing: backward compatibility shims, fallback mechanisms, bare `except: pass`, `deprecated`, `legacy`.

#### Tool Redirect (PreToolUse)

Redirects bash commands to proper tools: `grep/rg`→Grep, `find/fd`→Glob, `cat/head/tail`→Read, `sed/awk`→Edit.

#### Evasion Detection (Stop)

Uses z.ai GLM API to detect when the assistant defers work, shifts blame, minimizes problems, falsely claims completion, or silently skips failures.

## License

MIT
