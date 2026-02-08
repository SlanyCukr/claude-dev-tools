---
description: Parallel research synthesis
---

# /research

Spawn multiple research agents in parallel, combine findings into one opinionated recommendation.

## Usage

```
/research Best approach for real-time updates in our stack
/research How to handle file uploads with presigned URLs
/research State management options for the dashboard
/research Migration strategy from Prisma to Drizzle
```

## Workflow

```
1. Take research topic from user
2. Spawn 3 agents in parallel:
   ├── codebase-explorer → How does the codebase currently handle this / related patterns
   ├── web-research      → Current best practices, ecosystem state, common pitfalls
   └── context7-docs     → Library/framework documentation for relevant tools
3. Collect all findings
4. Synthesize into single opinionated recommendation
```

## Source Hierarchy

Not all sources are equal. Rate confidence by source:

| Source | Confidence | Why |
|--------|-----------|-----|
| Context7 (library docs) | HIGH | Official, versioned documentation |
| Official docs (web) | HIGH | Authoritative but may be outdated |
| Web search (verified) | MEDIUM | Cross-referenced with multiple sources |
| Web search (single source) | LOW | Could be outdated or opinionated |
| LLM training data | HYPOTHESIS | Treat as stale — verify against current docs |

**Key rule**: LLM training data is a hypothesis, not a fact. Always verify against current documentation.

## Output Format

Be **prescriptive, not exploratory**. Output says "Use X because Y", not "Consider X or Y".

```markdown
## Research: <topic>

### Recommendation
<clear, opinionated recommendation with reasoning>

### Current Codebase
<how the codebase handles this today, relevant patterns>

### Approach Details
<specifics of the recommended approach>

### Alternatives Considered
| Alternative | Why Not |
|-------------|---------|
| <option> | <concrete reason> |

### Pitfalls to Avoid
- <specific pitfall and how to avoid it>

### Confidence
- <aspect>: HIGH/MEDIUM/LOW — <reason>

### Gaps
- <anything we couldn't find or verify — honest reporting>
```

**Honest reporting**: "I couldn't find X" is valuable information. Don't paper over gaps.

## When to Use

- Before choosing a library or approach
- Evaluating migration strategies
- Understanding best practices for unfamiliar territory
- Comparing architectural options
- Before `/plan` when the approach isn't clear

## When NOT to Use

- You already know the approach → `/plan` or `/quick`
- Simple questions with obvious answers
- Project-specific questions (just explore the codebase)

## Context

$ARGUMENTS
