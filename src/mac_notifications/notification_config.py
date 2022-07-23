import uuid
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable, Optional


@dataclass
class NotificationConfig:
    title: str
    subtitle: Optional[str]
    text: Optional[str]
    icon: Optional[str]
    delay: timedelta
    notification_timeout: Optional[timedelta]
    action_button_str: Optional[str]
    action_button_callback: Optional[Callable[[], None]]
    reply_button_str: Optional[str]
    reply_callback: Optional[Callable[[str], None]]
    do_nothing_button_str: Optional[str]
    uid: str = field(default_factory=lambda: uuid.uuid4().hex)

    @property
    def contains_callback(self) -> bool:
        return bool(self.action_button_callback or self.reply_callback)

    @staticmethod
    def c_compliant(a_str: Optional[str]) -> Optional[str]:
        return "".join(filter(lambda x: bool(str.isalnum or str.isspace), a_str)) if a_str else None  # type: ignore

    def to_json_notification(self) -> "JSONNotificationConfig":
        return JSONNotificationConfig(
            title=NotificationConfig.c_compliant(self.title) or "Notification title",
            subtitle=NotificationConfig.c_compliant(self.subtitle),
            text=NotificationConfig.c_compliant(self.text),
            icon=self.icon,
            delay_in_seconds=(self.delay or timedelta()).total_seconds(),
            notification_timeout_in_seconds=(self.notification_timeout or timedelta()).total_seconds(),
            action_button_str=NotificationConfig.c_compliant(self.action_button_str),
            action_button_callback_present=bool(self.action_button_callback),
            reply_button_str=NotificationConfig.c_compliant(self.reply_button_str),
            reply_callback_present=bool(self.reply_callback),
            do_nothing_button_str=NotificationConfig.c_compliant(self.do_nothing_button_str),
            uid=self.uid,
        )


@dataclass
class JSONNotificationConfig:
    title: str
    subtitle: Optional[str]
    text: Optional[str]
    icon: Optional[str]
    delay_in_seconds: float
    notification_timeout_in_seconds: float
    action_button_str: Optional[str]
    action_button_callback_present: bool
    reply_button_str: Optional[str]
    reply_callback_present: bool
    do_nothing_button_str: Optional[str]
    uid: str

    @property
    def contains_callback(self) -> bool:
        return bool(self.action_button_callback_present or self.reply_callback_present)
