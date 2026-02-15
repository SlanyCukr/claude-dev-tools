"""TypeScript/JavaScript checker: comment stripping, Prettier, ESLint, tsc type checking."""

from __future__ import annotations

import json as _json
import re
import subprocess
from pathlib import Path

from . import CheckResult, find_ancestor_file, find_local_tool

# Preserve functional comments
_PRESERVE_PATTERN = re.compile(
    r"@ts-|eslint-|prettier-|TODO|FIXME|@type|@param|@returns"
)

# Match single-line comments
_SINGLE_LINE_COMMENT = re.compile(r"//.*$", re.MULTILINE)

# Match multi-line comments
_MULTI_LINE_COMMENT = re.compile(r"/\*[\s\S]*?\*/")


def _strip_comments(source: str) -> str:
    """Strip non-functional comments from JS/TS source via regex."""

    def _should_preserve(match: re.Match) -> str:
        text = match.group(0)
        if _PRESERVE_PATTERN.search(text):
            return text
        return ""

    result = _MULTI_LINE_COMMENT.sub(_should_preserve, source)
    result = _SINGLE_LINE_COMMENT.sub(
        lambda m: m.group(0) if _PRESERVE_PATTERN.search(m.group(0)) else "", result
    )
    return result


def check(file_path: str) -> list[CheckResult]:
    """Run TS/JS checks: comment strip, Prettier, ESLint (JSON), tsc type check."""
    results: list[CheckResult] = []
    path = Path(file_path)
    dir_ = path.parent

    if not find_ancestor_file(dir_, ["package.json"]):
        return results

    # 1. Strip comments
    try:
        original = path.read_text()
        stripped = _strip_comments(original)
        if stripped != original:
            path.write_text(stripped)
    except OSError:
        pass

    # 2. Prettier auto-format
    prettier = find_local_tool(dir_, "prettier")
    if prettier:
        try:
            subprocess.run(
                [prettier, "--write", file_path],
                capture_output=True, timeout=15, check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            pass

    # 3. ESLint (prefer local node_modules, structured JSON output)
    eslint = find_local_tool(dir_, "eslint")
    if eslint:
        try:
            result = subprocess.run(
                [eslint, "--format", "json", file_path],
                capture_output=True, text=True, timeout=15, check=False,
            )
            output = (result.stdout or "").strip()
            if output:
                try:
                    data = _json.loads(output)
                    errors: list[str] = []
                    for file_result in data:
                        for msg in file_result.get("messages", []):
                            severity = "error" if msg.get("severity") == 2 else "warning"
                            line = msg.get("line", 0)
                            rule = msg.get("ruleId") or ""
                            text = msg.get("message", "")
                            rule_str = f" [{rule}]" if rule else ""
                            errors.append(f"{path.name}:{line}: {severity}: {text}{rule_str}")
                    if errors:
                        results.append(CheckResult(tool="eslint", errors=errors))
                except _json.JSONDecodeError:
                    # Non-JSON output — parse raw lines
                    raw_errors = [line for line in output.splitlines() if line.strip()]
                    if raw_errors:
                        results.append(CheckResult(tool="eslint", errors=raw_errors))
        except (subprocess.TimeoutExpired, OSError):
            pass

    # 4. Type check: tsc --noEmit (filter to edited file only)
    tsconfig = find_ancestor_file(dir_, ["tsconfig.json", "tsconfig.app.json"])
    if tsconfig:
        tsc = find_local_tool(dir_, "tsc")
        if tsc:
            try:
                result = subprocess.run(
                    [tsc, "--noEmit"],
                    capture_output=True, text=True, timeout=30,
                    cwd=str(tsconfig.parent), check=False,
                )
                output = (result.stdout or "").strip()
                if output:
                    # Filter to only lines mentioning the edited file
                    fname = path.name
                    errors = [
                        line for line in output.splitlines()
                        if fname in line and line.strip()
                    ]
                    if errors:
                        results.append(CheckResult(tool="tsc", errors=errors))
            except (subprocess.TimeoutExpired, OSError):
                pass

    return results
