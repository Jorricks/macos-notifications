from __future__ import annotations

import time
from datetime import timedelta
from pathlib import Path

from mac_notifications import client


def notification_with_reply_button():
    client.create_notification(
        title="Cool notification",
        subtitle="Subtitle of the notification",
        text="Hello, I contain info",
        icon=Path(__file__).parent / "zoom.png",
        delay=timedelta(milliseconds=500),
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
        snooze_button_str="Or click me",
    )


if __name__ == "__main__":
    print("You have to press the notification within 10 seconds for it to work!")
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    notification_with_reply_button()
    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
