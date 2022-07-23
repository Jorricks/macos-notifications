import atexit
import time
from multiprocessing import Process, Queue
from threading import Thread
from typing import Dict, Optional, Tuple

from mac_notifications import notification_sender
from mac_notifications.notification_config import NotificationConfig
from mac_notifications.notification_process import NotificationProcess
from mac_notifications.singleton import Singleton

_NOTIFICATION_MAP: Dict[str, Tuple[Process, NotificationConfig]] = {}
_QUEUE: Queue = Queue()


class NotificationManager(metaclass=Singleton):
    def __init__(self):
        self.queue_updater: Optional[QueueUpdaterThread] = None

    def start_updater_object(self):
        if not (self.queue_updater and self.queue_updater.is_alive()):
            self.queue_updater = QueueUpdaterThread()
            self.queue_updater.start()

    def create_notification(self, notification_config: NotificationConfig) -> None:
        if not notification_config.contains_callback:
            notification_sender.send_notification(_QUEUE, notification_config.to_json_notification()).send()
        else:
            print(notification_config.uid)
            notification_process = NotificationProcess(_QUEUE, notification_config.to_json_notification())
            notification_process.start()
            _NOTIFICATION_MAP[notification_config.uid] = (notification_process, notification_config)
            self.start_updater_object()

    @staticmethod
    def get_active_running_notifications() -> int:
        return len([items[0].is_alive for items in _NOTIFICATION_MAP.values()])


class QueueUpdaterThread(Thread):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            drain_queue()
            if len(_NOTIFICATION_MAP) == 0:
                break
            time.sleep(0.1)

    @staticmethod
    def await_all_processes_to_be_finished() -> None:
        """This is a blocking operation to wait for all notifications to be fully handled before continuing."""
        for notification_uid, notification_tuple in _NOTIFICATION_MAP.items():
            notification_processes, notification_config = notification_tuple
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)


def drain_queue():
    while not _QUEUE.empty():
        notification_uid, event_id, reply_text = _QUEUE.get(block=True, timeout=1.0)
        print(notification_uid)
        if event_id == "action_button_clicked":
            notification_processes, notification_config = _NOTIFICATION_MAP.get(notification_uid)
            print(notification_config)
            notification_config.action_button_callback()
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)
        elif event_id == "reply_button_clicked":
            notification_processes, notification_config = _NOTIFICATION_MAP.get(notification_uid)
            notification_config.reply_callback(reply_text)
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)
        elif event_id == "done":
            _NOTIFICATION_MAP.pop(notification_uid)
        else:
            raise ValueError(f"Unknown {event_id=}.")


atexit.register(drain_queue)
