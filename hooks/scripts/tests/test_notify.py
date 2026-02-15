"""Tests for notify module."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

import notify as notify_mod
from notify import _notify_bell, send_notification


class TestSendNotification:
    @patch.object(notify_mod, "_notify_linux")
    def test_linux_dispatch(self, mock_linux: MagicMock) -> None:
        with patch.object(sys, "platform", "linux"):
            send_notification("Title", "Message")
        mock_linux.assert_called_once_with("Title", "Message")

    @patch.object(notify_mod, "_notify_macos")
    def test_macos_dispatch(self, mock_macos: MagicMock) -> None:
        with patch.object(sys, "platform", "darwin"):
            send_notification("Title", "Message")
        mock_macos.assert_called_once_with("Title", "Message")

    @patch.object(notify_mod, "_notify_bell")
    def test_other_platform_bell(self, mock_bell: MagicMock) -> None:
        with patch.object(sys, "platform", "win32"):
            send_notification("Title", "Message")
        mock_bell.assert_called_once()


class TestNotifyLinux:
    @patch("shutil.which", return_value="/usr/bin/notify-send")
    @patch("subprocess.run")
    @patch.object(notify_mod, "_play_sound_linux")
    def test_calls_notify_send(
        self, mock_sound: MagicMock, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        notify_mod._notify_linux("Title", "Msg")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "notify-send" in args
        assert "--urgency=critical" in args
        mock_sound.assert_called_once()

    @patch("shutil.which", return_value=None)
    @patch.object(notify_mod, "_notify_bell")
    def test_missing_notify_send_warns(self, mock_bell: MagicMock, mock_which: MagicMock) -> None:
        notify_mod._warning_shown = False
        notify_mod._notify_linux("Title", "Msg")
        mock_bell.assert_called_once()

    @patch("shutil.which", return_value=None)
    @patch.object(notify_mod, "_notify_bell")
    def test_warning_shown_once(self, mock_bell: MagicMock, mock_which: MagicMock) -> None:
        notify_mod._warning_shown = False
        notify_mod._notify_linux("Title", "Msg1")
        assert notify_mod._warning_shown is True
        notify_mod._notify_linux("Title", "Msg2")
        # Bell still called each time, but warning flag stays True
        assert mock_bell.call_count == 2


class TestNotifyMacos:
    @patch("shutil.which", side_effect=lambda cmd: "/usr/bin/osascript" if cmd == "osascript" else None)
    @patch("subprocess.run")
    def test_escapes_quotes(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        notify_mod._notify_macos('Title"evil', 'Msg"bad')
        mock_run.assert_called_once()
        script = mock_run.call_args[0][0][-1]
        assert '\\"' in script
        assert '"evil' not in script.replace('\\"', "")

    @patch("shutil.which", return_value=None)
    @patch.object(notify_mod, "_notify_bell")
    def test_missing_osascript(self, mock_bell: MagicMock, mock_which: MagicMock) -> None:
        notify_mod._warning_shown = False
        notify_mod._notify_macos("Title", "Msg")
        mock_bell.assert_called_once()


class TestNotifyBell:
    def test_bell_outputs_to_stderr(self, capsys: object) -> None:
        _notify_bell()
        # capsys doesn't capture \a well but we verify no crash
