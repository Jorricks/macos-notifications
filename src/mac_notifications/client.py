from __future__ import annotations

import logging
from datetime import timedelta
from pathlib import Path
from typing import Callable

from mac_notifications.manager import Notification, NotificationManager
from mac_notifications.notification_config import NotificationConfig

"""
This serves as the entrypoint for our users. They should only need to use this file.
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_notification_manager() -> NotificationManager:
    """Return the NotificationManager object."""
    return NotificationManager()


def stop_listening_for_callbacks() -> None:
    return get_notification_manager().cleanup()


def create_notification(
    title: str = "Notification",
    subtitle: str | None = None,
    text: str | None = None,
    icon: str | Path | None = None,
    sound: str | None = None,
    delay: timedelta = timedelta(),
    action_button_str: str | None = None,
    action_callback: Callable[[], None] | None = None,
    reply_button_str: str | None = None,
    reply_callback: Callable[[str], None] | None = None,
    snooze_button_str: str | None = None,
) -> Notification :
    """
    Create a MacOS notification :)
    :param title: Title of the notification.
    :param subtitle: The subtitle of the notification.
    :param text: The text/main body of the notification.
    :param icon: An Icon you would like to set on the right bottom.
    :param delay: Delay before showing the message.
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
        sound=sound,
        delay=delay,
        action_button_str=action_button_str,
        action_callback=action_callback,
        reply_button_str=reply_button_str,
        reply_callback=reply_callback,
        snooze_button_str=snooze_button_str,
    )
    return get_notification_manager().create_notification(notification_config)
