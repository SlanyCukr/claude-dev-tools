"""Python checker: comment stripping, ruff auto-fix + lint, basedpyright/pyright type checking."""

from __future__ import annotations

import io
import subprocess
import tokenize
from pathlib import Path

from . import CheckResult, find_ancestor_file, has_command

# Comment prefixes to preserve (functional comments)
_PRESERVE_PREFIXES = (
    "# type:", "# noqa", "# ruff:", "# fmt:", "# TODO", "# FIXME",
    "# pragma:", "# pylint:", "# pyright:",
)


def _strip_comments(source: str) -> str:
    """Strip non-functional comments from Python source using tokenize."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except tokenize.TokenError:
        return source

    # Collect comment token positions to remove
    remove_ranges: list[tuple[int, int, int, int]] = []
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            text = tok.string.strip()
            if not any(text.startswith(p) for p in _PRESERVE_PREFIXES):
                remove_ranges.append((*tok.start, *tok.end))

    if not remove_ranges:
        return source

    lines = source.splitlines(keepends=True)
    for srow, scol, erow, ecol in reversed(remove_ranges):
        # tokenize uses 1-based line numbers
        line_idx = srow - 1
        if line_idx < len(lines):
            line = lines[line_idx]
            # If comment is the entire line (after stripping), remove the line
            if line.strip().startswith("#"):
                lines[line_idx] = ""
            else:
                # Remove inline comment
                lines[line_idx] = line[:scol].rstrip() + "\n"

    return "".join(lines)


def check(file_path: str) -> list[CheckResult]:
    """Run Python checks: comment strip, ruff auto-fix, ruff lint, type check."""
    results: list[CheckResult] = []
    path = Path(file_path)
    dir_ = path.parent

    if not find_ancestor_file(dir_, ["pyproject.toml", "setup.py", "setup.cfg"]):
        return results

    # 1. Strip comments
    try:
        original = path.read_text()
        stripped = _strip_comments(original)
        if stripped != original:
            path.write_text(stripped)
    except OSError:
        pass

    # 2. Auto-fix: import sorting + format
    if has_command("ruff"):
        try:
            subprocess.run(
                ["ruff", "check", "--select", "I,RUF022", "--fix", file_path],
                capture_output=True, timeout=10, check=False,
            )
            subprocess.run(
                ["ruff", "format", file_path],
                capture_output=True, timeout=10, check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            pass

        # 3. Lint check
        try:
            result = subprocess.run(
                ["ruff", "check", "--output-format=concise", file_path],
                capture_output=True, text=True, timeout=10, check=False,
            )
            output = (result.stdout or "").strip()
            if output:
                errors = [line for line in output.splitlines() if line.strip()]
                results.append(CheckResult(tool="ruff", errors=errors, fixed=True))
        except (subprocess.TimeoutExpired, OSError):
            pass

    # 4. Type check (basedpyright preferred, pyright fallback)
    type_cmd = None
    if has_command("basedpyright"):
        type_cmd = "basedpyright"
    elif has_command("pyright"):
        type_cmd = "pyright"

    if type_cmd:
        try:
            result = subprocess.run(
                [type_cmd, "--outputjson", file_path],
                capture_output=True, text=True, timeout=30, check=False,
            )
            if result.stdout:
                import json
                try:
                    data = json.loads(result.stdout)
                    diagnostics = data.get("generalDiagnostics", [])
                    errors = []
                    for d in diagnostics:
                        severity = d.get("severity", "")
                        if severity in ("error", "warning"):
                            rng = d.get("range", {})
                            start = rng.get("start", {})
                            line = start.get("line", 0) + 1
                            msg = d.get("message", "")
                            rule = d.get("rule", "")
                            rule_str = f" [{rule}]" if rule else ""
                            errors.append(f"{path.name}:{line}: {msg}{rule_str}")
                    if errors:
                        results.append(CheckResult(tool=type_cmd, errors=errors))
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, OSError):
            pass

    return results
