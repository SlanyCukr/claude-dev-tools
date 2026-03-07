#!/usr/bin/env python3
"""Stop hook: detect evasion patterns in assistant's last response via DashScope API.

Returns JSON {"decision": "block", "reason": "..."} when evasion is detected,
which forces Claude Code to continue working instead of stopping.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _util import is_waiting_for_user_input, read_hook_stdin

API_URL = "https://coding-intl.dashscope.aliyuncs.com/v1/chat/completions"
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
MODEL = "glm-4.7"
TIMEOUT_SECONDS = 30

EVASION_PROMPT = """\
You are a quality gate evaluating whether an AI coding assistant should stop working.

Read the assistant's last response carefully. Check for these evasion patterns:
- DEFERRAL: Pushing work to later, follow-up, or next session
- BLAME SHIFTING: Claiming failures are pre-existing or unrelated
- MINIMIZING: Calling problems minor, edge cases, or good enough
- FALSE COMPLETION: Claiming done while tests fail or requirements unmet
- SILENT SKIPPING: Not mentioning known failures

If no evasion patterns are found, respond with exactly: {"ok": true}
If any pattern is detected, respond with: {"ok": false, "reason": "describe the specific patterns found"}

You MUST respond with ONLY a JSON object. No markdown, no explanation, no code fences."""


def get_last_assistant_text(transcript_path: str) -> str:
    """Extract the last assistant message text from the transcript."""
    try:
        lines = Path(transcript_path).read_text().strip().split("\n")
    except OSError:
        return ""

    for line in reversed(lines):
        try:
            entry = json.loads(line)
            msg = entry.get("message")
            if not msg or msg.get("role") != "assistant":
                continue
            content = msg.get("content", [])
            if isinstance(content, list):
                texts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        texts.append(block["text"])
                if texts:
                    return "\n".join(texts)
            elif isinstance(content, str):
                return content
        except json.JSONDecodeError:
            continue
    return ""


def parse_json_response(text: str) -> dict | None:
    """Parse JSON from model response, stripping markdown fences if present."""
    text = text.strip()
    if text.startswith("```"):
        # Strip ```json ... ``` fences
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def call_llm(assistant_text: str) -> dict | None:
    """Call DashScope API to check for evasion patterns. Returns parsed JSON or None."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": EVASION_PROMPT},
            {"role": "user", "content": f"Assistant's response:\n\n{assistant_text[:8000]}"},
        ],
        "max_tokens": 500,
        "temperature": 0,
    }).encode()

    req = urllib.request.Request(API_URL, data=body, headers=headers)
    resp = urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS)
    result = json.loads(resp.read())
    content = result["choices"][0]["message"].get("content", "")
    if not content:
        raise ValueError("LLM returned empty content")
    parsed = parse_json_response(content)
    if parsed is None:
        raise ValueError(f"Failed to parse LLM response as JSON: {content[:200]}")
    return parsed


def main() -> int:
    data = read_hook_stdin()
    if not data:
        return 0

    # Don't block if already in a stop-hook retry loop
    if data.get("stop_hook_active"):
        return 0

    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        return 0

    # Don't block if waiting for user input
    if is_waiting_for_user_input(transcript_path):
        return 0

    assistant_text = get_last_assistant_text(transcript_path)
    if not assistant_text:
        return 0

    try:
        result = call_llm(assistant_text)
    except Exception as e:
        reason = f"Evasion checker error: {e}"
        print(json.dumps({"decision": "block", "reason": reason}))
        return 0

    if result.get("ok") is False:
        reason = result.get("reason", "Evasion pattern detected")
        print(json.dumps({"decision": "block", "reason": reason}))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
