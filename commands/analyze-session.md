---
description: Analyze session to suggest skill/workflow improvements
argument-hint: <session-id>
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, TodoWrite
---

# Self-Improvement Session Analyzer

You are a self-improvement agent analyzing a Claude Code session to synthesize suggestions for improving skills, workflows, and CLAUDE.md files.

## Session to Analyze

Session ID: $1

**First, validate the session ID is provided.** If `$1` is empty or missing, show usage and list recent sessions (see Error Handling section).

## Step 1: Convert Session to TOON

First, convert the session transcript to TOON format for efficient analysis.

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/session-to-toon.sh" "$1" /tmp/session-analysis.toon
```

Run this command, then read the output file.

## Step 2: Analyze the TOON Transcript

After reading the TOON file, analyze it for these patterns:

### 2.1 Repeated Patterns → New Skills
Look for:
- Tool sequences repeated 3+ times (e.g., Grep → Read → Edit)
- Workarounds used multiple times
- Multi-step processes that could be codified
- Error recovery patterns that worked

### 2.2 Errors/Frustrations → CLAUDE.md Updates
Look for:
- Tool failures and how they were resolved
- User clarifications needed (indicates missing context)
- Misunderstandings about project structure
- Commands that failed and required correction

### 2.3 Tool Usage Patterns → Workflow Improvements
Look for:
- Inefficient tool usage (could have used X instead of Y)
- Missing tool combinations that would help
- Patterns that should be documented

### 2.4 Questions Asked → Missing Context
Look for:
- Questions about codebase structure
- Questions about conventions
- Questions about how things work
- Information that should be in CLAUDE.md

### 2.5 Successful Workflows → Documentation
Look for:
- Smooth multi-step processes
- Effective debugging approaches
- Good patterns worth preserving

## Step 3: Generate Suggestions

For each finding, generate a concrete suggestion:

### For New Skills
Generate a complete SKILL.md with:
```markdown
---
name: "Skill Name"
description: "When to use this skill"
allowed-tools: ["Tool1", "Tool2"]
---

# Skill Name

## When to Use
[Specific triggers]

## Tags
[Keywords]

## Quick Start
[Step-by-step process]

## Example
[Concrete example from the session]
```

### For CLAUDE.md Updates
Generate a diff showing:
- What section to add/modify
- The exact content to add
- Why this helps (based on session evidence)

### For Workflow Improvements
Generate documentation showing:
- The improved workflow
- Before vs after comparison
- When to apply it

## Step 4: Interactive Approval

Present each suggestion to the user one at a time using AskUserQuestion:

For each suggestion:
1. Show the suggestion type (Skill / CLAUDE.md Update / Workflow)
2. Show the evidence from the session that motivated it
3. Show the full proposed content
4. Ask: "Apply this suggestion?"
   - Options: "Yes, apply it", "Skip this one", "Edit before applying", "Stop reviewing"

## Step 5: Apply Approved Suggestions

For approved suggestions:

### Skills
- Create directory: `~/.claude/skills/<skill-name>/`
- Write: `~/.claude/skills/<skill-name>/SKILL.md`

### CLAUDE.md Updates
- Check if update is for root (`~/.claude/CLAUDE.md`) or project (`./CLAUDE.md`)
- Apply the diff using Edit tool

### Workflows
- Add to appropriate CLAUDE.md or create in `~/.claude/workflows/`

## Step 6: Summary Report

After all suggestions are processed, provide a summary:
- Total suggestions found
- Suggestions applied
- Suggestions skipped
- Files created/modified

## Important Guidelines

1. **Be specific**: Base all suggestions on actual evidence from the session
2. **Be actionable**: Every suggestion should be immediately usable
3. **Be conservative**: Only suggest changes that clearly add value
4. **Preserve context**: Include session excerpts that motivated each suggestion
5. **Respect existing patterns**: Match the style of existing skills and CLAUDE.md

## Error Handling

If the session ID is not provided or invalid:
- Show usage: `/analyze-session <session-id>`
- List recent sessions: `ls -t ~/.claude/projects/*/*.jsonl | head -10`

If the TOON conversion fails:
- Show the error
- Suggest checking if the session ID is correct

## Start Now

Begin by running the TOON conversion command for session: $1
