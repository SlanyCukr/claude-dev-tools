#!/usr/bin/env python3
"""
UserPromptSubmit hook to inject subagent guidance when spec-kit commands are detected.
Provides context-specific reminders about which subagents to use.
"""

import json
import sys
import re

SPECKIT_GUIDANCE = {
    "specify": """
## Subagent Guidance for speckit.specify
- Launch `zai-speckit-plugin:codebase-explorer` to understand existing code patterns before writing spec
- Look for similar features, naming conventions, file structure
- Run exploration in parallel with reading the feature description
""",
    "clarify": """
## Subagent Guidance for speckit.clarify
- Use `zai-speckit-plugin:web-research` to research options and best practices
- Use `zai-speckit-plugin:context7-docs` to check library capabilities and API signatures
- Run both in parallel if multiple clarifications needed
""",
    "plan": """
## Subagent Guidance for speckit.plan

### Research Phase (parallel)
- `zai-speckit-plugin:codebase-explorer` - Analyze existing patterns and implementations
- `zai-speckit-plugin:web-research` - Best practices and architectural patterns
- `zai-speckit-plugin:context7-docs` - Library/framework documentation

### Architecture Phase
- `zai-speckit-plugin:architect` - For complex features requiring system design decisions or ADRs

### Validation Phase (after plan is written)
- `zai-speckit-plugin:plan-refiner` - Check plan against `docs/rules/` conventions
- Fix CRITICAL/HIGH severity violations before proceeding to implement
""",
    "tasks": """
## Subagent Guidance for speckit.tasks
- `zai-speckit-plugin:codebase-explorer` - Understand file structure for accurate task breakdown
- `zai-speckit-plugin:architect` - Help structure complex features into logical phases
- Consider existing patterns when defining implementation files
""",
    "implement": """
## Subagent Guidance for speckit.implement

### Choose the Right Build Agent
- `zai-speckit-plugin:python-build-agent` - Python/backend (type hints, Ruff/mypy)
- `zai-speckit-plugin:react-nextjs-agent` - React/Next.js frontend (TanStack Query, TypeScript)
- `zai-speckit-plugin:build-agent` - Other languages/general purpose

### Quality Agents (use proactively)
- `zai-speckit-plugin:tdd-guide` - Write tests FIRST before implementation
- `zai-speckit-plugin:code-reviewer` - After each phase of changes
- `zai-speckit-plugin:security-reviewer` - After security-sensitive code (auth, input handling, API endpoints)
- `zai-speckit-plugin:e2e-runner` - For UI features needing E2E tests

### Task Prompt Format
DO NOT paste task descriptions - agent reads files.

```
Task(python-build-agent, "Task: T012 - Define PRIORITY_SCENARIOS
Context: specs/001-llm-tests/
Code: backend/tests/llm_integration/helpers/scenarios.py")
```

### Execution Strategy
1. Parse tasks.md for task IDs, target files, [P] markers
2. For each task: tdd-guide first (write test) → build agent (implement) → code-reviewer
3. Launch parallel subagents for tasks marked [P]
4. After security-sensitive changes: security-reviewer
5. After UI changes: e2e-runner if user flows affected
6. Mark completed tasks [X] in tasks.md
""",
    "review": """
## Subagent Guidance for speckit.review
Post-implementation review phase:

- `zai-speckit-plugin:code-reviewer` - Code quality, bugs, anti-patterns
- `zai-speckit-plugin:security-reviewer` - OWASP Top 10, secrets, vulnerabilities
- `zai-speckit-plugin:tdd-guide` - Verify test coverage >= 80%

Run all three in parallel for efficiency.
""",
}


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = input_data.get("prompt", "").lower()

    # Detect spec-kit commands
    context_parts = []

    for command, guidance in SPECKIT_GUIDANCE.items():
        # Match patterns like: /speckit.specify, speckit.plan, "run speckit.implement"
        pattern = rf"(?:^|[\s/])speckit\.{command}\b"
        if re.search(pattern, prompt):
            context_parts.append(guidance.strip())

    if context_parts:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n\n".join(context_parts),
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
