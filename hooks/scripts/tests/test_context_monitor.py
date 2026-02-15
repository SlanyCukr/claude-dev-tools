"""Tests for context_monitor hook."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from context_monitor import (
    calculate_context_usage,
    get_warning_level,
    load_state,
    save_state,
)


class TestCalculateContextUsage:
    def test_all_fields(self) -> None:
        usage = {
            "input_tokens": 50000,
            "cache_creation_input_tokens": 30000,
            "cache_read_input_tokens": 20000,
        }
        assert calculate_context_usage(usage) == 100000

    def test_missing_fields(self) -> None:
        usage = {"input_tokens": 50000}
        assert calculate_context_usage(usage) == 50000

    def test_empty_usage(self) -> None:
        assert calculate_context_usage({}) == 0

    def test_none_values(self) -> None:
        usage = {
            "input_tokens": None,
            "cache_creation_input_tokens": 10000,
            "cache_read_input_tokens": None,
        }
        assert calculate_context_usage(usage) == 10000


class TestGetWarningLevel:
    def test_below_threshold(self) -> None:
        assert get_warning_level(30.0) is None

    def test_at_40(self) -> None:
        assert get_warning_level(40.0) == 40

    def test_at_60(self) -> None:
        assert get_warning_level(60.0) == 60

    def test_at_75(self) -> None:
        assert get_warning_level(75.0) == 75

    def test_at_80(self) -> None:
        assert get_warning_level(80.0) == 80

    def test_at_85(self) -> None:
        assert get_warning_level(85.0) == 85

    def test_at_90(self) -> None:
        assert get_warning_level(90.0) == 90

    def test_at_95(self) -> None:
        assert get_warning_level(95.0) == 95

    def test_between_thresholds(self) -> None:
        assert get_warning_level(72.0) == 60

    def test_at_100(self) -> None:
        assert get_warning_level(100.0) == 95


class TestThresholdDedup:
    def test_save_and_load_state(self, tmp_path: Path) -> None:
        with patch("context_monitor.STATE_DIR", tmp_path):
            state = {"shown_thresholds": [40, 60], "lastWarningTime": 1000.0}
            save_state("test-session", state)
            loaded = load_state("test-session")
        assert loaded["shown_thresholds"] == [40, 60]
        assert loaded["lastWarningTime"] == 1000.0

    def test_load_missing_state(self, tmp_path: Path) -> None:
        with patch("context_monitor.STATE_DIR", tmp_path):
            loaded = load_state("nonexistent")
        assert loaded == {}

    def test_dedup_prevents_repeat(self, tmp_path: Path) -> None:
        with patch("context_monitor.STATE_DIR", tmp_path):
            state = {"shown_thresholds": [40], "lastWarningTime": 0}
            save_state("sess", state)
            loaded = load_state("sess")
            assert 40 in loaded["shown_thresholds"]
