import time
from datetime import timedelta
from pathlib import Path

from mac_notifications import client


if __name__ == "__main__":
    print("You have to press the notification within 30 seconds for it to work.")
    client.create_notification(
        title="Cool notification",
        subtitle="Subtitle of the notification",
        text="Hello, I contain info",
        icon=Path(__file__).parent / "img" / "chat.png",
        delay=timedelta(milliseconds=500),
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
        snooze_button_str="Or click me",
    )
    time.sleep(30)
    client.stop_listening_for_callbacks()
