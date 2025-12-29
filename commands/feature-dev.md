---
description: Context-efficient feature development workflow. Use for adding new features to any codebase.
argument-hint: <feature description>
allowed-tools: Bash, Write, Edit, Read, Glob, Grep, AskUserQuestion, TodoWrite, Task
---

# Context-Efficient Feature Development

You are implementing a new feature. This workflow prioritizes context efficiency - use subagents for exploration, load files just-in-time.

## Feature Request

$ARGUMENTS

## CRITICAL RULES

1. **Delegate exploration** - Use lean-explore agent, don't read files yourself during discovery
2. **Just-in-time loading** - Read files only when implementing that specific component
3. **Use anchors** - The exploration result gives you exact file:line references, use them
4. **Target: <5k tokens** before implementation begins

---

## Phase 1: Discovery (~500 tokens)

### 1.1 Understand the Request
- Is this a backend feature, frontend feature, or both?
- What is the core functionality?
- What data does it need to store/fetch?

### 1.2 Create Todo List
```
- [ ] Discovery - understand requirements
- [ ] Exploration - launch lean-explore agent
- [ ] Architecture - design components using anchors
- [ ] Clarifying questions
- [ ] Implementation
- [ ] Review
- [ ] Summary
```

### 1.3 Determine Scope
Use AskUserQuestion if unclear:
- Backend only? Frontend only? Both?
- Database changes required?
- Integration with existing features?

---

## Phase 2: Exploration (via lean-explore agent)

### 2.1 Create Exploration Brief

```markdown
# Exploration Brief

## Goal
- Primary objective: [what feature we're building]
- Definition of done: [what success looks like]

## Mode
[backend | frontend | schema | fullstack]

## Focus Areas (prioritize)
1. Similar existing features to use as templates
2. Patterns for [specific component type]
3. Integration points with existing features

## Questions to Answer
1. Which existing feature is the best template?
2. What patterns are used for [X]?
3. Are there any conventions or gotchas to follow?
4. What files need to be modified for integration?

## Entry Points (if known)
- Files to start from: [any known files, or empty]

## Constraints
- Must match existing code style
- [any project-specific constraints from CLAUDE.md]
```

### 2.2 Launch Agent

```
Launch lean-explore agent with the brief above
```

### 2.3 Receive Anchors

The agent returns:
- **Anchors**: File paths + line ranges + why they matter
- **Patterns**: Conventions to follow
- **Risks**: Gotchas to watch for
- **Suggested implementation order**

**Store these anchors for Phase 5.**

---

## Phase 3: Architecture (~500 tokens)

### 3.1 Use Anchors
Based on lean-explore results, you now know:
- Which feature to use as template
- Exact files and line ranges to reference
- Patterns to follow

**DO NOT re-read files.** Use the anchors.

### 3.2 Sketch Component List
List files to create with estimated line counts:

```markdown
## Files to Create

### Backend (if applicable)
- `router.py` (~50 lines) - API endpoints
- `service.py` (~80 lines) - Business logic
- `schemas.py` (~40 lines) - Request/response models
- [other files based on project patterns]

### Frontend (if applicable)
- `components/feature-component.tsx` (~100 lines)
- `hooks/use-feature.ts` (~40 lines)
- `index.ts` (~10 lines) - Public API
```

### 3.3 Confirm with User
Use AskUserQuestion to confirm the approach.

---

## Phase 4: Clarifying Questions (~500 tokens)

### MANDATORY - DO NOT SKIP

Before implementing, ask about:
- **Edge cases**: What happens when X fails?
- **Error handling**: How should errors be displayed?
- **Scope boundaries**: What's NOT included?
- **Integration**: How does this connect to existing features?

Wait for answers before proceeding.

---

## Phase 5: Implementation

### 5.1 Choose Implementation Strategy

**Option A: Implement yourself** (small/simple features)
- Few files to create
- Clear patterns from anchors
- You have enough context

**Option B: Delegate to impl agent** (larger/complex features)
- Multiple components (backend + frontend)
- Want to preserve your context for orchestration
- Bounded units with clear contracts

For Option B, you can run multiple impl agents in parallel (e.g., backend and frontend simultaneously) if the interface contract is defined first.

### 5.2 Option A: Implement Yourself

Follow the "Suggested Implementation Order" from lean-explore:
1. Database model (if needed)
2. Backend: data layer → business logic → API
3. Frontend: hooks → components → page integration

For EACH component:
1. **Check your anchors** - Find the relevant file + line range
2. **Read ONLY the relevant lines** - Don't read whole files
3. **Write the component** - Follow the pattern from anchor
4. **Mark todo complete**

### 5.3 Option B: Delegate to impl Agent

Create an Implementation Brief for each bounded unit:

```markdown
# Implementation Brief

## Goal
- [What to build in 1-2 sentences]
- Definition of done: [specific outcome]

## Scope
- Create: [files to create]
- Modify: [files to modify]
- Do NOT touch: [off-limits files]

## Decisions Already Made
- [Key decision 1 and WHY]
- [Key decision 2 and WHY]

## Anchors
| File | Lines | Symbol | Why |
|------|-------|--------|-----|
[paste relevant anchors from lean-explore]

## Interface Contract
[API routes, schemas, types - if applicable]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Tests pass: `[test command]`

## Question Protocol
If blocked, ask with: (1) what you tried (2) 2-3 options (3) your recommendation
```

Launch the agent:
```
Launch impl agent with the brief above
```

### 5.4 Handle impl Agent Response

**If Ship (success):**
- Review the summary of changes
- Verify integration points
- Mark component complete, continue to next

**If Ask (needs clarification):**
- Answer the question or pick from options
- Re-launch impl with the answer added to brief

**If Fail (blocked):**
- Review evidence and what was tried
- Either fix the blocker yourself or re-scope

### 5.5 Integration Points

After all components are done, check project's CLAUDE.md for:
- Router/route registration
- Model registration (for ORMs)
- Any other integration requirements

Handle integration yourself (don't delegate) - this requires cross-component awareness.

---

## Phase 6: Review (~1,000 tokens)

### 6.1 Type Check & Lint
Run the project's type checker and linter (check CLAUDE.md or package.json/pyproject.toml for commands).

### 6.2 Fix Issues
Address any errors immediately.

### 6.3 Basic Testing
If tests exist, run them.

---

## Phase 7: Summary

### 7.1 Complete Todos
Mark all items complete.

### 7.2 Provide Summary
- What was built
- Files created/modified
- How to test the feature
- Suggested next steps

---

## Context Budget Reference

| Phase | Main Agent Tokens | Notes |
|-------|------------------|-------|
| Discovery | ~500 | Understanding request |
| Exploration | ~200 | Brief sent to lean-explore (Haiku) |
| Anchors received | ~800 | Structured result from lean-explore |
| Architecture | ~500 | Using anchors, minimal reads |
| Questions | ~500 | Clarifications |
| **Pre-implementation** | **~2,500** | |

**Implementation options:**

| Strategy | Tokens per Component | Best For |
|----------|---------------------|----------|
| Implement yourself | ~500-1000 | Small features, few files |
| Delegate to impl (Sonnet) | ~300 (brief + result) | Large features, parallel work |

| Phase | Main Agent Tokens | Notes |
|-------|------------------|-------|
| Review | ~1,000 | Type checking, linting |
| Integration | ~500 | Router registration, wiring |

**Why this works**:
- lean-explore (Haiku) reads files in its own context
- impl (Sonnet) writes code in its own context
- You only receive structured briefs and results

---

## Start Now

Begin with Phase 1: Read the feature request and create your todo list.
