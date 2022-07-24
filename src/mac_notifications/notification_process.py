from __future__ import annotations

from multiprocessing import Process, SimpleQueue

from mac_notifications import notification_sender
from mac_notifications.notification_config import JSONNotificationConfig


class NotificationListenerProcess(Process):
    """
    This is a simple process to launch a notification in a separate process.

    Why you may ask?
    Waiting for the Callback is a blocking operation.
    Because it is a blocking operation, if we want to be able to receive Callbacks from multiple notifications at once,
    we need to open them in separate processes (I tried threads first, but that doesn't work :'( ). Also, if we want to
    be able to launch these notifications with a callback in the background while running my own application(e.g. a
    calender application) without freezing, we must run it in a separate process as well.
    """
    def __init__(self, queue: SimpleQueue, notification_config: JSONNotificationConfig):
        super().__init__()
        self.notification_config = notification_config
        self._queue = queue

    def run(self) -> None:
        notification_sender.create_notification(self._queue, self.notification_config, True).send()
        # on if any of the callbacks are provided, start the event loop (this will keep the program from stopping)
