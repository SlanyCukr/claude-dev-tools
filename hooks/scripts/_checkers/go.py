"""Go checker: comment stripping, gofmt, go vet, golangci-lint."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from . import CheckResult, find_ancestor_file, has_command

# Preserve functional comments
_PRESERVE_PATTERN = re.compile(r"//nolint|//go:|TODO|FIXME")

_SINGLE_LINE_COMMENT = re.compile(r"//.*$", re.MULTILINE)
_MULTI_LINE_COMMENT = re.compile(r"/\*[\s\S]*?\*/")


def _strip_comments(source: str) -> str:
    """Strip non-functional comments from Go source via regex."""

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
    """Run Go checks: comment strip, gofmt, go vet, golangci-lint."""
    results: list[CheckResult] = []
    path = Path(file_path)
    dir_ = path.parent

    if not find_ancestor_file(dir_, ["go.mod"]):
        return results

    # 1. Strip comments
    try:
        original = path.read_text()
        stripped = _strip_comments(original)
        if stripped != original:
            path.write_text(stripped)
    except OSError:
        pass

    # 2. gofmt auto-format
    if has_command("gofmt"):
        try:
            subprocess.run(
                ["gofmt", "-w", file_path],
                capture_output=True, timeout=10, check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            pass

    # 3. go vet
    if has_command("go"):
        try:
            result = subprocess.run(
                ["go", "vet", file_path],
                capture_output=True, text=True, timeout=15, check=False,
            )
            output = (result.stderr or "").strip()
            if output:
                errors = [line for line in output.splitlines() if line.strip()]
                results.append(CheckResult(tool="go-vet", errors=errors))
        except (subprocess.TimeoutExpired, OSError):
            pass

    # 4. golangci-lint
    if has_command("golangci-lint"):
        try:
            result = subprocess.run(
                ["golangci-lint", "run", "--fast", file_path],
                capture_output=True, text=True, timeout=15, check=False,
            )
            output = (result.stdout or result.stderr or "").strip()
            if output:
                errors = [line for line in output.splitlines() if line.strip()]
                results.append(CheckResult(tool="golangci-lint", errors=errors))
        except (subprocess.TimeoutExpired, OSError):
            pass

    return results
