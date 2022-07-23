from datetime import timedelta
from pathlib import Path
from typing import Callable, Optional, Union

from mac_notifications.notification_config import NotificationConfig
from mac_notifications.notification_manager import NotificationManager


def get_notification_manager() -> NotificationManager:
    return NotificationManager()


def create_notification(
    title: str = "Notification",
    subtitle: Optional[str] = None,
    text: Optional[str] = None,
    icon: Optional[Union[str, Path]] = None,
    delay: timedelta = timedelta(),
    notification_timeout: Optional[timedelta] = None,
    action_button_str: Optional[str] = None,
    action_button_callback: Optional[Callable[[], None]] = None,
    reply_button_str: Optional[str] = None,
    reply_callback: Optional[Callable[[str], None]] = None,
    do_nothing_button_str: Optional[str] = None,
):
    notification_config = NotificationConfig(
        title=title,
        subtitle=subtitle,
        text=text,
        icon=(str(icon.resolve()) if isinstance(icon, Path) else icon) if icon else None,
        delay=delay,
        notification_timeout=notification_timeout,
        action_button_str=action_button_str,
        action_button_callback=action_button_callback,
        reply_button_str=reply_button_str,
        reply_callback=reply_callback,
        do_nothing_button_str=do_nothing_button_str,
    )
    get_notification_manager().create_notification(notification_config)
