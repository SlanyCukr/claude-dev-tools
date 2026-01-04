#!/usr/bin/env python3
"""SessionStart hook: inject subagent philosophy for main session only."""
import json

SUBAGENT_PHILOSOPHY = """
## Subagent Usage Philosophy

**Subagent usage is PIVOTAL for preserving main session context.** The main session should orchestrate, not execute heavy work.

### Why Subagents
- Main session context is precious - every token counts
- Subagents run in isolation - their token usage doesn't pollute main context
- Parallelization - multiple subagents can work simultaneously
- Specialization - each agent has focused expertise

### Small Chunks Only
**Give each subagent ONE small, focused task.** When subagents receive large chunks of work:
- They become "lazy" and implement only part of the work
- They lose focus and quality degrades
- They may silently skip steps

**Good:** "Implement T1: Create User model in models/user.py"
**Bad:** "Implement all 5 tasks from the plan"

### Honesty Over Completion
**Not completing work is NOT an error.** The only error is:
- Doing partial work without clearly stating it
- Claiming "done" when steps were skipped
- Silent failures or omissions

### Early Bail Pattern
Subagents will return early (without doing work) if:
- Task is unclear → they'll ask for clarification
- Task is too broad → they'll suggest how to split it
- Context risk is high → they'll suggest narrowing scope
- Confidence is low → they'll explain their concerns

**This is GOOD behavior** - it prevents wasted work and poor quality output.
""".strip()

output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": SUBAGENT_PHILOSOPHY
    }
}
print(json.dumps(output))
