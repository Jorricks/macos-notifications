from asyncio import Queue
from multiprocessing import Process

from mac_notifications import notification_sender
from mac_notifications.notification_config import JSONNotificationConfig


class NotificationProcess(Process):
    def __init__(self, queue: Queue, notification_config: JSONNotificationConfig):
        super().__init__()
        self.notification_config = notification_config
        self._queue = queue

    def run(self) -> None:
        notification_sender.send_notification(self._queue, self.notification_config).send()
        # on if any of the callbacks are provided, start the event loop (this will keep the program from stopping)

