---
name: jira
description: Interact with Jira issues using jira-cli - view, list, create, edit issues and add comments with token-efficient output
allowed-tools: Bash
---

# Jira CLI Skill

Interact with Jira using the `jira` CLI tool. All commands use `--plain` format for token efficiency.

## Setup (already configured)

- **Binary**: `~/.factory/bin/jira` (in PATH via ~/.zshrc)
- **Config**: `~/.config/.jira/.config.yml`
- **Credentials**: `~/.netrc` (no need to export JIRA_API_TOKEN)
- **Server**: https://idcapps.atlassian.net/
- **Default project**: INTGR

## Token-Efficient Output

Always use these flags for compact output:
- `--plain` - Tab-separated output (most efficient)
- `--columns field1,field2` - Limit to needed fields only
- `--no-headers` - Skip column headers when parsing

## Commands Reference

### View Single Issue

```bash
jira issue view ISSUE-123 --plain
```

With specific fields:
```bash
jira issue view ISSUE-123 --plain --comments 5
```

### List Issues

List assigned to me:
```bash
jira issue list -a$(jira me) --plain
```

With filters:
```bash
jira issue list \
  -a"assignee@email.com" \
  -s"In Progress" \
  -tBug \
  -yHigh \
  --plain \
  --columns KEY,SUMMARY,STATUS,PRIORITY
```

Filter flags:
- `-a` / `--assignee` - Filter by assignee
- `-s` / `--status` - Filter by status
- `-t` / `--type` - Filter by type (Bug, Story, Task, Epic)
- `-y` / `--priority` - Filter by priority (High, Medium, Low)
- `-l` / `--label` - Filter by label
- `-p` / `--project` - Filter by project
- `-q` / `--jql` - Custom JQL query

### Create Issue

```bash
jira issue create \
  -tStory \
  -s"Issue summary" \
  -b"Issue description" \
  -pPROJECT \
  -yHigh \
  --no-input
```

With epic:
```bash
jira issue create -tStory -s"Summary" -PEPIC-42 --no-input
```

Flags:
- `-t` / `--type` - Issue type (required)
- `-s` / `--summary` - Issue summary (required)
- `-b` / `--body` - Description
- `-p` / `--project` - Project key
- `-y` / `--priority` - Priority
- `-P` / `--parent` - Parent epic key
- `-l` / `--label` - Labels (can repeat)
- `-C` / `--component` - Component
- `-a` / `--assignee` - Assignee
- `--custom` - Custom fields (e.g., `--custom story-points=3`)
- `--no-input` - Non-interactive mode

### Edit Issue

```bash
jira issue edit ISSUE-123 \
  -s"New summary" \
  -yHigh \
  -lbug \
  -lurgent \
  --no-input
```

Same flags as create, plus:
- `-S` / `--status` - Transition to status

### Add Comment

```bash
jira issue comment add ISSUE-123 "Comment body" --no-input
```

From stdin:
```bash
echo "Comment text" | jira issue comment add ISSUE-123 --no-input
```

### Move/Transition Issue

```bash
jira issue move ISSUE-123 "In Progress"
```

List available transitions:
```bash
jira issue move ISSUE-123 --plain
```

### Assign Issue

```bash
jira issue assign ISSUE-123 "user@email.com"
```

Assign to self:
```bash
jira issue assign ISSUE-123 $(jira me)
```

### Sprint Operations

List sprints:
```bash
jira sprint list --plain
```

Current sprint issues:
```bash
jira sprint list --current --plain
```

### Epic Operations

List epics:
```bash
jira epic list --plain --columns KEY,SUMMARY,STATUS
```

Add issue to epic:
```bash
jira epic add EPIC-1 ISSUE-123
```

## Common Workflows

### Quick status check
```bash
jira issue list -a$(jira me) -s"In Progress" --plain --columns KEY,SUMMARY
```

### Create bug with details
```bash
jira issue create \
  -tBug \
  -s"Bug title" \
  -b"Steps to reproduce..." \
  -yHigh \
  -lbug \
  --no-input
```

### Update and comment
```bash
jira issue edit ISSUE-123 -S"In Review" --no-input
jira issue comment add ISSUE-123 "Ready for review" --no-input
```

## Output Parsing

Plain output is tab-separated. Parse with:
```bash
jira issue list --plain --no-headers | while IFS=$'\t' read -r key summary status; do
  echo "Issue: $key - $summary ($status)"
done
```

## Error Handling
