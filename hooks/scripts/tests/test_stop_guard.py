"""Tests for stop_guard hook."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from stop_guard import find_unchecked_tasks, load_block_state, save_block_state


class TestFindUncheckedTasks:
    def test_no_plans_dir(self, tmp_path: Path) -> None:
        with patch("stop_guard.Path.home", return_value=tmp_path):
            name, tasks = find_unchecked_tasks("/some/project")
        assert name == ""
        assert tasks == []

    def test_finds_unchecked_tasks(self, tmp_path: Path) -> None:
        plans_dir = tmp_path / ".claude" / "plans"
        plans_dir.mkdir(parents=True)
        plan = plans_dir / "plan.md"
        plan.write_text(
            "/some/project\n"
            "- [x] Done task\n"
            "- [ ] Pending task 1\n"
            "- [ ] Pending task 2\n"
        )
        with patch("stop_guard.Path.home", return_value=tmp_path):
            name, tasks = find_unchecked_tasks("/some/project")
        assert name == "plan.md"
        assert len(tasks) == 2
        assert "Pending task 1" in tasks[0]

    def test_ignores_unrelated_plan(self, tmp_path: Path) -> None:
        plans_dir = tmp_path / ".claude" / "plans"
        plans_dir.mkdir(parents=True)
        plan = plans_dir / "other.md"
        plan.write_text(
            "/workspace/alpha-app\n"
            "- [ ] Some task\n"
        )
        with patch("stop_guard.Path.home", return_value=tmp_path):
            name, tasks = find_unchecked_tasks("/workspace/beta-app")
        assert name == ""
        assert tasks == []

    def test_all_checked_returns_empty(self, tmp_path: Path) -> None:
        plans_dir = tmp_path / ".claude" / "plans"
        plans_dir.mkdir(parents=True)
        plan = plans_dir / "done.md"
        plan.write_text(
            "/some/project\n"
            "- [x] Task 1\n"
            "- [x] Task 2\n"
        )
        with patch("stop_guard.Path.home", return_value=tmp_path):
            name, tasks = find_unchecked_tasks("/some/project")
        assert name == ""
        assert tasks == []


class TestEscapeHatch:
    def test_save_and_load_state(self, tmp_path: Path) -> None:
        with patch("stop_guard.STATE_DIR", tmp_path):
            state = {"last_block_time": time.time()}
            save_block_state("test-session", state)
            loaded = load_block_state("test-session")
        assert "last_block_time" in loaded

    def test_load_missing_state(self, tmp_path: Path) -> None:
        with patch("stop_guard.STATE_DIR", tmp_path):
            loaded = load_block_state("nonexistent")
        assert loaded == {}


class TestUserInputDetection:
    def test_waiting_for_input(self, tmp_path: Path) -> None:
        from _util import is_waiting_for_user_input

        transcript = tmp_path / "transcript.jsonl"
        entry = {
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "tool_use", "name": "AskUserQuestion", "input": {}}
                ],
            }
        }
        transcript.write_text(json.dumps(entry) + "\n")
        assert is_waiting_for_user_input(str(transcript)) is True

    def test_not_waiting(self, tmp_path: Path) -> None:
        from _util import is_waiting_for_user_input

        transcript = tmp_path / "transcript.jsonl"
        entry = {
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Done!"}
                ],
            }
        }
        transcript.write_text(json.dumps(entry) + "\n")
        assert is_waiting_for_user_input(str(transcript)) is False
