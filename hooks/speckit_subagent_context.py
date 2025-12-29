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
- Launch `Explore` subagent to understand existing code patterns before writing spec
- Look for similar features, naming conventions, file structure
- Run exploration in parallel with reading the feature description
""",
    "clarify": """
## Subagent Guidance for speckit.clarify
- Use `web-research` to research options and best practices
- Use `context7-docs` to check library capabilities and API signatures
- Run both in parallel if multiple clarifications needed
""",
    "plan": """
## Subagent Guidance for speckit.plan
- Launch `Explore` to analyze codebase patterns and existing implementations
- Use `web-research` for best practices and architectural patterns
- Use `context7-docs` for library/framework documentation
- Run all three in parallel for efficiency:
  Task(Explore, "Find existing patterns for [feature]")
  Task(web-research, "[topic] best practices")
  Task(context7-docs, "[library] [specific APIs]")
""",
    "implement": """
## Subagent Guidance for speckit.implement
IMPORTANT: Delegate each task to a `build-agent` subagent:
- Parse tasks.md for the task list
- Launch parallel `build-agent` subagents for tasks marked [P]
- Sequential tasks: wait for dependencies before launching
- After each phase: run `code-reviewer` on changes

Example parallel execution:
```
Task(build-agent, "Implement T1: [task] in [file] per specs/[feature]/plan.md")
Task(build-agent, "Implement T2: [task] in [file] per specs/[feature]/plan.md")
```
After completion, mark tasks [X] in tasks.md.
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
