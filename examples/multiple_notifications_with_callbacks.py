import time
from pathlib import Path

from mac_notifications import client


if __name__ == "__main__":
    print("Sending meeting notification.")
    client.create_notification(
        title="Meeting starts now.",
        subtitle="Standup Data Team",
        icon=Path(__file__).parent / "img" / "zoom.png",
        action_button_str="Join zoom meeting",
        action_callback=lambda: print("Joining zoom meeting now."),
    )

    time.sleep(5)
    print("Sending notification.")
    client.create_notification(
        title="Message from Henk",
        subtitle="Hey Dude, are we still meeting?",
        icon=Path(__file__).parent / "img" / "chat.png",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"You replied: {reply}"),
    )
    print("Yet another message.")
    client.create_notification(
        title="Message from Daniel",
        subtitle="How you doing?",
        icon=Path(__file__).parent / "img" / "chat.png",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"You replied: {reply}"),
    )

    print("Application will remain active until both notifications have been answered.")
    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
    client.stop_listening_for_callbacks()
