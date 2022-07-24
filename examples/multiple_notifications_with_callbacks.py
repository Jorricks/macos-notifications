import time
from mac_notifications import client


if __name__ == "__main__":
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    client.create_notification(
        title="Action notification",
        subtitle="Subtitle of the notification",
        action_button_str="Perform an action",
        action_callback=lambda: print("Pressed action button"),
    )

    time.sleep(1)
    client.create_notification(
        title="Reply notification",
        subtitle="Subtitle of the notification",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
    )

    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
        print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    client.stop_listening_for_callbacks()
