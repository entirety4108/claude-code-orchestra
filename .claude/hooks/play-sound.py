#!/usr/bin/env python3
"""
Hook: Play sound on Stop (response complete) and Notification (user attention needed).

Stop hook       → Windows Notify.wav  (soft completion chime)
Notification hook → Windows Exclamation.wav  (attention sound)
"""
import json
import subprocess
import sys

SOUNDS = {
    "stop": r"C:\Windows\Media\Windows Notify.wav",
    "notification": r"C:\Windows\Media\Windows Exclamation.wav",
}


def play_wav(path: str) -> None:
    """Play a wav file asynchronously via PowerShell."""
    subprocess.Popen(
        [
            "powershell", "-NoProfile", "-NonInteractive", "-c",
            f"(New-Object Media.SoundPlayer '{path}').PlaySync()",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    try:
        data = json.load(sys.stdin)
        event = data.get("hook_event_name", "").lower()

        if event == "stop":
            play_wav(SOUNDS["stop"])
        elif event == "notification":
            play_wav(SOUNDS["notification"])

    except Exception:
        pass  # Never block Claude on sound errors


if __name__ == "__main__":
    main()
