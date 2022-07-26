# Examples

On this page we will list several examples. Let's start with a demonstration of the last example of this page.

<p align="center">
<a href="#Multiple notifications"><img src="../img/example-run.gif" alt="macos-notifications" width="800px"></a>
</p>

## Simple notification
```python
from mac_notifications import client


if __name__ == "__main__":
    client.create_notification(
        title="Meeting starts now!",
        subtitle="Team Standup"
    )
```


## Notification with a reply callback
```python
from __future__ import annotations

import time
from datetime import timedelta
from pathlib import Path

from mac_notifications import client


if __name__ == "__main__":
    print("You have to press the notification within 30 seconds for it to work.")
    client.create_notification(
        title="Cool notification",
        subtitle="Subtitle of the notification",
        text="Hello, I contain info",
        icon=Path(__file__).parent / "zoom.png",
        delay=timedelta(milliseconds=500),
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
        snooze_button_str="Or click me",
    )
    time.sleep(30)
    client.stop_listening_for_callbacks()
```

## Notification with an action
```python
from __future__ import annotations

import time
from functools import partial
from pathlib import Path

from mac_notifications import client


def join_zoom_meeting(conf_number: int | str) -> None:
    """Join the zoom meeting"""
    # import subprocess
    # subprocess.run(f'open "zoommtg://zoom.us/join?action=join&confno={conf_number}&browser=chrome"', shell=True)
    print(f"Opened zoom into meeting with {conf_number=}.")


if __name__ == "__main__":
    print(client.get_notification_manager().get_active_running_notifications())
    client.create_notification(
        title="Meeting starts now!",
        subtitle="Standup time :)",
        icon=Path(__file__).parent / "zoom.png",
        action_button_str="Join zoom meeting",
        action_callback=partial(join_zoom_meeting, conf_number="12345678"),
    )
    time.sleep(30)
    client.stop_listening_for_callbacks()
```


## Multiple notifications
Give this a try. Play around with the notifications.
Notice that when you close the notification, the count doesn't go down and the application stays running forever.
This is one of the limitations of using Python for these notifications as we don't know whether the notification is 
still present or not.
```python
import time
from mac_notifications import client


if __name__ == "__main__":
    print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    client.create_notification(
        title="Action notification",
        subtitle="Subtitle of the notification",
        action_button_str="Perform an action",
        action_callback=lambda: print("Pressed action button"),
    )

    time.sleep(1)
    client.create_notification(
        title="Reply notification",
        subtitle="Subtitle of the notification",
        reply_button_str="Reply to this notification",
        reply_callback=lambda reply: print(f"Replied {reply=}"),
    )

    while client.get_notification_manager().get_active_running_notifications() > 0:
        time.sleep(1)
        print(f"Active number of notifications: {client.get_notification_manager().get_active_running_notifications()}")
    client.stop_listening_for_callbacks()
```