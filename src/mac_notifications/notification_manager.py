from __future__ import annotations

import atexit
import time
from multiprocessing import Process, Queue
from threading import Thread
from typing import Dict, Tuple, Final

from mac_notifications import notification_sender
from mac_notifications.notification_config import NotificationConfig
from mac_notifications.notification_process import NotificationProcess
from mac_notifications.singleton import Singleton

"""
This is the module responsible for managing the notifications over time & enabling callbacks to be executed.
"""

# The _NOTIFICATION_MAP is required to keep track of notifications that have a callback. We map the UID of the
# notification to the process that was started for it and the configuration.
_NOTIFICATION_MAP: Dict[str, Tuple[Process, NotificationConfig]] = {}
# The _CALLBACK_QUEUE is required to tell our CallbackExecutorThread that is needs to execute a callback of a specific
# notification. The CallbackExecutorThread is constantly monitoring this queue for any new callback it needs to execute.
_CALLBACK_QUEUE: Final[Queue] = Queue()


class NotificationManager(metaclass=Singleton):
    """
    The NotificationManager is responsible for managing the notifications. This includes the following:
    - Starting new notifications.
    - Starting the Callback Executor thread in the background.
    """
    def __init__(self):
        self.callback_executor: CallbackExecutorThread | None = None

    def start_queue_updater_thread(self):
        if not (self.callback_executor and self.callback_executor.is_alive()):
            self.callback_executor = CallbackExecutorThread()
            self.callback_executor.start()

    def create_notification(self, notification_config: NotificationConfig) -> None:
        if not notification_config.contains_callback:
            notification_sender.create_notification(_CALLBACK_QUEUE, notification_config.to_json_notification()).send()
        else:
            print(f"Creating notification for: {notification_config.uid}")
            notification_process = NotificationProcess(_CALLBACK_QUEUE, notification_config.to_json_notification())
            notification_process.start()
            _NOTIFICATION_MAP[notification_config.uid] = (notification_process, notification_config)
            self.start_queue_updater_thread()

    @staticmethod
    def get_active_running_notifications() -> int:
        return len([items[0].is_alive for items in _NOTIFICATION_MAP.values()])


class CallbackExecutorThread(Thread):
    """
    Background threat that checks each 0.1 second whether there are any callbacks that it should execute.
    """
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            drain_queue()
            if len(_NOTIFICATION_MAP) == 0:
                break
            time.sleep(0.1)

    @staticmethod
    def await_all_notification_processes_to_be_finished() -> None:
        """This is a blocking operation to wait for all notifications to be fully handled before continuing."""
        for notification_uid, notification_tuple in _NOTIFICATION_MAP.items():
            notification_processes, notification_config = notification_tuple
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)


def drain_queue() -> None:
    """
    This drains the Callback Queue. When there is a notification for which a callback should be fired, this event is
    added to the `_CALLBACK_QUEUE`. This background Threat is then responsible for listening in on the _CALLBACK_QUEUE
    and when there is a callback it should execute, it executes it.
    """
    while not _CALLBACK_QUEUE.empty():
        notification_uid, event_id, reply_text = _CALLBACK_QUEUE.get(block=True, timeout=1.0)
        print(notification_uid)
        if event_id == "action_button_clicked":
            notification_processes, notification_config = _NOTIFICATION_MAP.get(notification_uid)
            print(f"Execution action callback for {notification_config}")
            # @ToDo(jorrick enable this again)
            # notification_config.action_callback()
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)
        elif event_id == "reply_button_clicked":
            notification_processes, notification_config = _NOTIFICATION_MAP.get(notification_uid)
            print(f"Executing reply callback for {notification_config}")
            # @ToDo(jorrick enable this again)
            # notification_config.reply_callback(reply_text)
            notification_processes.join()
            _NOTIFICATION_MAP.pop(notification_uid)
        elif event_id == "done":
            _NOTIFICATION_MAP.pop(notification_uid)
        else:
            raise ValueError(f"Unknown event_id: {event_id}.")


atexit.register(drain_queue)
