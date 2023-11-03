import time
from pathlib import Path

from mac_notifications import client
from mac_notifications.client import Notification


if __name__ == "__main__":
    print("Sending meeting notification.")

    sent: list[Notification] = []

    def cancel_all():
        for i in sent:
            i.cancel()

    sent.append(client.create_notification(
        title="Annoyed by notifications?",
        icon=Path(__file__).parent / "img" / "zoom.png",
        action_button_str="Cancel all notifications",
        action_callback=cancel_all,
    ))

    time.sleep(5)
    print("Sending notification.")
    sent.append(client.create_notification(
        title="Message from Henk",
        subtitle="Hey Dude, are we still meeting?",
        icon=Path(__file__).parent / "img" / "chat.png",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"You replied to Henk: {reply}"),
    ))

    print("Yet another message.")
    sent.append(client.create_notification(
        title="Message from Daniel",
        subtitle="How you doing?",
        icon=Path(__file__).parent / "img" / "chat.png",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"You replied to Daniel: {reply}"),
    ))
    time.sleep(5)

    for i in sent:
        i.cancel()
        time.sleep(5)

    print("Application will remain active until both notifications have been answered.")
    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
    print("all notifications are handled")
    client.stop_listening_for_callbacks()
