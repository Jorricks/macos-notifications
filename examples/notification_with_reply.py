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
        notification_timeout=timedelta(seconds=10),
        reply_button_str="Reply to me",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
        do_nothing_button_str="Or click me",
    )


if __name__ == "__main__":
    print(client.get_notification_manager().get_active_running_notifications())
    notification_with_reply_button()
    print(client.get_notification_manager().get_active_running_notifications())
    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(2)
        print(client.get_notification_manager().get_active_running_notifications())
