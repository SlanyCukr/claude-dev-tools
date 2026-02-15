"""Modular checker subpackage for file_checker hook."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    """Result from a single checker tool (ruff, eslint, pyright, etc.)."""

    tool: str
    errors: list[str] = field(default_factory=list)
    fixed: bool = False

    def summary(self, max_errors: int = 10) -> str:
        """Format errors for output, truncating beyond max_errors."""
        if not self.errors:
            return ""
        prefix = f"[{self.tool}]"
        if self.fixed:
            prefix += " (auto-fixed, remaining)"
        lines = self.errors[:max_errors]
        if len(self.errors) > max_errors:
            lines.append(f"... and {len(self.errors) - max_errors} more errors")
        return f"{prefix}\n" + "\n".join(lines)


def find_ancestor_file(start: Path, filenames: list[str]) -> Path | None:
    """Walk up from start directory to find a file by name."""
    current = start
    while True:
        for fname in filenames:
            candidate = current / fname
            if candidate.exists():
                return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def find_local_tool(dir_: Path, tool_name: str) -> str | None:
    """Check node_modules/.bin/ first, then global PATH. Returns path or None."""
    # Walk up looking for node_modules/.bin/
    current = dir_
    while True:
        local = current / "node_modules" / ".bin" / tool_name
        if local.exists():
            return str(local)
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Fall back to global
    global_path = shutil.which(tool_name)
    return global_path


def has_command(cmd: str) -> bool:
    """Check if a command is available on PATH."""
    return shutil.which(cmd) is not None


def is_test_file(file_path: str) -> bool:
    """Check if file is a test file."""
    name = Path(file_path).name
    stem = Path(file_path).stem

    # Python
    if name.endswith(".py"):
        if stem.startswith("test_") or stem.endswith("_test"):
            return True

    # JS/TS
    if name.endswith((".test.ts", ".spec.ts", ".test.tsx", ".spec.tsx",
                      ".test.js", ".spec.js", ".test.jsx", ".spec.jsx")):
        return True

    # Go
    if name.endswith("_test.go"):
        return True

    # Directory-based
    dir_path = Path(file_path).parent.as_posix()
    if "/__tests__/" in dir_path or dir_path.endswith("/__tests__"):
        return True

    return False
