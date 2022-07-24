import time
from datetime import timedelta
from mac_notifications import client


def notification_with_action_button() -> None:
    """Create a notification for a meeting."""
    client.create_notification(
        title="Action notification",
        subtitle="Subtitle of the notification",
        callback_timeout=timedelta(seconds=20),
        action_button_str="Perform an action",
        action_callback=lambda: print(f"Pressed action button"),
    )


def notification_with_reply_button():
    client.create_notification(
        title="Reply notification",
        subtitle="Subtitle of the notification",
        callback_timeout=timedelta(seconds=20),
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
    )


if __name__ == "__main__":
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    notification_with_reply_button()
    time.sleep(5)
    notification_with_action_button()
    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
