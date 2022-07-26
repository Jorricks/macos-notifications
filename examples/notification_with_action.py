from __future__ import annotations

import time
from functools import partial
from pathlib import Path

from mac_notifications import client


def join_a_meeting(conf_number: int | str) -> None:
    print(f"Joining meeting with conf_number='{conf_number}'.")


if __name__ == "__main__":
    print("You have to press the notification within 30 seconds for it to work.")
    client.create_notification(
        title="Meeting starts now!",
        subtitle="Standup. Join please.",
        icon=Path(__file__).parent / "img" / "zoom.png",
        action_button_str="Join zoom meeting",
        action_callback=partial(join_a_meeting, conf_number="12345678"),
    )
    time.sleep(30)
    client.stop_listening_for_callbacks()
