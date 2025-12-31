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
- Launch `zai-speckit-plugin:codebase-explorer` subagent to understand existing code patterns before writing spec
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
- Launch `zai-speckit-plugin:codebase-explorer` to analyze codebase patterns and existing implementations
- Use `zai-speckit-plugin:web-research` for best practices and architectural patterns
- Use `zai-speckit-plugin:context7-docs` for library/framework documentation
- Run all three in parallel for efficiency:
  Task(zai-speckit-plugin:codebase-explorer, "Find existing patterns for [feature]")
  Task(web-zai-speckit-plugin:web-research, "[topic] best practices")
  Task(zai-speckit-plugin:context7-docs, "[library] [specific APIs]")
""",
    "implement": """
## Subagent Guidance for speckit.implement
IMPORTANT: Delegate each task to a `zai-speckit-plugin:build-agent` subagent.

### Task Prompt Format (CRITICAL)
Use build-agent's expected format. DO NOT paste task descriptions - agent reads files.

**BAD** (pastes full description):
```
Task(build-agent, "Implement T012 [US1] Define 10+ PRIORITY_SCENARIOS covering high/medium/low classifications with expected_priority field mapping to HIGH/MEDIUM/LOW enum values...")
```

**GOOD** (structured format - agent reads spec files):
```
Task(build-agent, "Task: T012 - Define PRIORITY_SCENARIOS
Context: specs/001-llm-tests/
Code: backend/tests/llm_integration/helpers/scenarios.py")
```

### Execution Strategy
- Parse tasks.md to identify task IDs, target files, and [P] markers
- Launch parallel subagents for tasks marked [P] (same phase, no dependencies)
- Sequential tasks: wait for dependencies before launching
- After each phase: run `zai-speckit-plugin:code-reviewer` on changes
- Mark completed tasks [X] in tasks.md
""",
    "tasks": """
## Subagent Guidance for speckit.tasks
- May need `Explore` to understand file structure for accurate task breakdown
- Consider existing patterns when defining implementation files
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
