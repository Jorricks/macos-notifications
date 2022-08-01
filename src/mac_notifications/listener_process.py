from __future__ import annotations

from multiprocessing import Process, SimpleQueue

from mac_notifications import notification_sender
from mac_notifications.notification_config import JSONNotificationConfig


class NotificationProcess(Process):
    """
    This is a simple process to launch a notification in a separate process.

    Why you may ask?
    First, the way we need to launch a notification using a class, this class can only be instantiated once in a
    process. Hence, for simple notifications we create a new process and then immediately stop it after the notification
    was launched.
    Second, waiting for the user interaction with a notification is a blocking operation.
    Because it is a blocking operation, if we want to be able to receive any user interaction from the notification,
    without completely halting/freezing our main process, we need to open it in a background process.
    """

    def __init__(self, notification_config: JSONNotificationConfig, queue: SimpleQueue | None):
        super().__init__()
        self.notification_config = notification_config
        self.queue = queue

    def run(self) -> None:
        notification_sender.create_notification(self.notification_config, self.queue).send()
        # on if any of the callbacks are provided, start the event loop (this will keep the program from stopping)
