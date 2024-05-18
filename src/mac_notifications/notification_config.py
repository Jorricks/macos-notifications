from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable

"""
The dataclasses that represent a Notification configuration.
"""


@dataclass
class NotificationConfig:
    """
    The standard representation of a Notifications. This is used inside the main process.
    """

    title: str
    subtitle: str | None
    text: str | None
    icon: str | None
    delay: timedelta
    action_button_str: str | None
    action_callback: Callable[[], None] | None
    reply_button_str: str | None
    reply_callback: Callable[[str], None] | None
    snooze_button_str: str | None
    sound: str | None
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def contains_callback(self) -> bool:
        return bool(self.action_callback or self.reply_callback)

    @staticmethod
    def c_compliant(a_str: str | None) -> str | None:
        return "".join(filter(lambda x: bool(str.isalnum or str.isspace), a_str)) if a_str else None  # type: ignore

    def to_json_notification(self) -> "JSONNotificationConfig":
        return JSONNotificationConfig(
            title=NotificationConfig.c_compliant(self.title) or "Notification title",
            subtitle=NotificationConfig.c_compliant(self.subtitle),
            text=NotificationConfig.c_compliant(self.text),
            icon=self.icon,
            sound=self.sound,
            delay_in_seconds=(self.delay or timedelta()).total_seconds(),
            action_button_str=NotificationConfig.c_compliant(self.action_button_str),
            action_callback_present=bool(self.action_callback),
            reply_button_str=NotificationConfig.c_compliant(self.reply_button_str),
            reply_callback_present=bool(self.reply_callback),
            snooze_button_str=NotificationConfig.c_compliant(self.snooze_button_str),
            uid=self.uid,
        )


@dataclass
class JSONNotificationConfig:
    """
    This notification configuration class that only contains serializable parts.

    This class is required because waiting for user interaction with a notification is a blocking operation.
    Because it is a blocking operation, if we want to be able to receive any user interaction from the notification,
    without completely halting/freezing our main process, we need to open it in a background process. However, to be
    able to transfer the data from the notification to the other process, all the arguments should be serializable. As
    callbacks/functions are not serializable, we replaced them by booleans on whether it contained a callback or not.
    Once a callback should be triggered, we send a message over a multiprocessing Queue and trigger the callback in
    the main process.
    """

    title: str
    subtitle: str | None
    text: str | None
    icon: str | None
    sound: str | None
    delay_in_seconds: float
    action_button_str: str | None
    action_callback_present: bool
    reply_button_str: str | None
    reply_callback_present: bool
    snooze_button_str: str | None
    uid: str

    @property
    def contains_callback(self) -> bool:
        return bool(self.action_callback_present or self.reply_callback_present)
