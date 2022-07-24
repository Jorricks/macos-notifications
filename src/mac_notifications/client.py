from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import Callable

from mac_notifications.notification_config import NotificationConfig
from mac_notifications.notification_manager import NotificationManager

"""
This serves as the entrypoint for our users. They should only need to use this file.
"""


def get_notification_manager() -> NotificationManager:
    """Return the NotificationManager object."""
    return NotificationManager()


def create_notification(
    title: str = "Notification",
    subtitle: str | None = None,
    text: str | None = None,
    icon: str | Path | None = None,
    delay: timedelta = timedelta(),
    callback_timeout: timedelta | None = None,
    action_button_str: str | None = None,
    action_callback: Callable[[], None] | None = None,
    reply_button_str: str | None = None,
    reply_callback: Callable[[str], None] | None = None,
    snooze_button_str: str | None = None,
) -> None:
    """
    Create a MacOS notification :)
    :param title: Title of the notification.
    :param subtitle: The subtitle of the notification.
    :param text: The text/main body of the notification.
    :param icon: An Icon you would like to set on the right bottom.
    :param delay: Delay before showing the message.
    :param callback_timeout: The time to wait for the callback to happen. This is only required when you set
    `action_callback` or `reply_callback`. It's important that you set this right as each notification with a
    callback spawns in a separate process which takes ~5MB Ram and 0.1%CPU usage. If you have max 10 notifications a
    day, you can set this to 24 hours. If you expect a notification each minute, you should set this to max an hour.
    :param action_button_str: The string of the Action button.
    :param action_callback: The function to call when the action button is pressed.
    :param reply_button_str: The string of the Reply button.
    :param reply_callback: The function to call with the replied text.
    :param snooze_button_str: This is a useless button that closes the notification (but not the process). Think of
    this as a snooze button.
    """
    notification_config = NotificationConfig(
        title=title,
        subtitle=subtitle,
        text=text,
        icon=(str(icon.resolve()) if isinstance(icon, Path) else icon) if icon else None,
        delay=delay,
        callback_timeout=callback_timeout,
        action_button_str=action_button_str,
        action_callback=action_callback,
        reply_button_str=reply_button_str,
        reply_callback=reply_callback,
        snooze_button_str=snooze_button_str,
    )
    get_notification_manager().create_notification(notification_config)
