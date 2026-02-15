---
description: Code quality + security review in one pass
---

# /review

Combined code quality and security review. Runs code-reviewer and security-reviewer in parallel, then synthesizes findings.

## Usage

```
/review src/services/user.py
/review src/api/
/review git diff
/review Review the changes from the last 3 commits
```

## Workflow

```
1. Determine scope (files, directory, or git diff)
2. Spawn 2 agents in parallel:
   |-- code-reviewer    -> Bugs, anti-patterns, quality issues
   +-- security-reviewer -> OWASP Top 10, secrets, vulnerabilities
3. Synthesize findings into single prioritized report
```

## Scope Determines Depth

| Scope | What Happens |
|-------|--------------|
| Single file | Both agents review the file |
| Directory | Both agents review recent changes in directory |
| `git diff` | Both agents review uncommitted changes |
| Commit range | Both agents review changes across commits |

## Output Format

```markdown
## Review: <scope>

### Critical (fix now)
- [SECURITY] <issue> in <file:line>
- [BUG] <issue> in <file:line>

### High (fix before merge)
- [QUALITY] <issue> in <file:line>

### Medium (consider fixing)
- [QUALITY] <issue> in <file:line>

### Positive
- <what's done well>
```

## When to Use

- After implementing a feature (before committing)
- Before opening a pull request
- After a code change you want a second opinion on
- Regular code health checks

## When NOT to Use

- Deep security audit with remediation -> `/security` with "full audit"
- You only want one type of review -> call the agent directly

## Related

- Agents: agents/code-reviewer.md, agents/security-reviewer.md
- Rules: rules/security.md
