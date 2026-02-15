#!/usr/bin/env python3
"""Cross-platform OS notifications with sound. Fire-and-forget with thread timeout."""

from __future__ import annotations

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

_warning_shown = False
_TIMEOUT_SECONDS = 3


def send_notification(title: str, message: str) -> None:
    """Send an OS notification with sound. Falls back to terminal bell."""
    if sys.platform == "linux":
        _notify_linux(title, message)
    elif sys.platform == "darwin":
        _notify_macos(title, message)
    else:
        _notify_bell()


def _run_with_timeout(func: object, *args: object) -> None:
    """Run a callable in a thread with a timeout to avoid blocking."""
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(func, *args)  # type: ignore[arg-type]
        try:
            future.result(timeout=_TIMEOUT_SECONDS)
        except Exception:  # noqa: BLE001
            pass


def _play_sound_linux() -> None:
    """Fire-and-forget sound on Linux via paplay."""
    if shutil.which("paplay"):
        try:
            subprocess.Popen(  # noqa: S603
                ["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass


def _notify_linux(title: str, message: str) -> None:
    global _warning_shown  # noqa: PLW0603

    if not shutil.which("notify-send"):
        if not _warning_shown:
            _warning_shown = True
            print("notify: notify-send not found, using terminal bell", file=sys.stderr)
        _notify_bell()
        return

    def _send() -> None:
        subprocess.run(
            [
                "notify-send",
                "--app-name=Claude",
                "--urgency=critical",
                title,
                message,
            ],
            capture_output=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )

    _run_with_timeout(_send)
    _play_sound_linux()


def _notify_macos(title: str, message: str) -> None:
    global _warning_shown  # noqa: PLW0603

    if not shutil.which("osascript"):
        if not _warning_shown:
            _warning_shown = True
            print("notify: osascript not found, using terminal bell", file=sys.stderr)
        _notify_bell()
        return

    # Escape quotes to prevent injection in osascript
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    safe_message = message.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'display notification "{safe_message}" '
        f'with title "{safe_title}" sound name "Glass"'
    )

    def _send() -> None:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )

    _run_with_timeout(_send)

    # Fire-and-forget sound via afplay
    if shutil.which("afplay"):
        try:
            subprocess.Popen(  # noqa: S603
                ["afplay", "/System/Library/Sounds/Glass.aiff"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass


def _notify_bell() -> None:
    print("\a", end="", file=sys.stderr)
