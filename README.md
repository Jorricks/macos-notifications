<p align="center">
  <a href="https://github.com/Jorricks/macos-notifications"><img src="https://github.com/Jorricks/macos-notifications/raw/main/docs/macos-notifications.png" alt="macos-notifications" width="600px"></a>
</p>
<p align="center">
<p align="center">
<a href="https://www.apple.com/mac/" target="_blank">
    <img src="https://img.shields.io/badge/Platform-mac-blue" alt="Mac supported">
</a>
<a href="https://python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python 3.7+ supported">
</a>
</p>

---

**Documentation**: [https://jorricks.github.io/macos-notifications/](https://jorricks.github.io/macos-notifications/)

**Source Code**: [https://github.com/Jorricks/macos-notifications](https://github.com/Jorricks/macos-notifications)

---

**mac-notification** is a Python library to make it as easy as possible to create interactable notifications.

## Features
- 🚀 Easy python interface. It's as simple as '`client.create_notification(title="Meeting starts now!", subtitle="Team Standup")`'
- 💥 Ability to add action buttons with callbacks!
- 📝 Ability to reply to notifications!
- ⌚ Delayed notifications.
- ⏱️ Automatically time out the notification listener.
- 📦 Just two packages (which is really just one package) as a dependency

## Installation

To use macos-notifications, first install it using pip:

    pip install macos-notifications

## Requirements
Python 3.8+

Mac-notification only relies on `pyobjc`:
- The [PyObjC project](https://pyobjc.readthedocs.io/) aims to provide a bridge between the Python and Objective-C programming languages on macOS.

## Example
A simple example. Please look [in the docs](https://jorricks.github.io/macos-notifications/) for more examples.

```python
from pathlib import Path
from mac_notifications import client

client.create_notification(
    title="Meeting starts now!",
    subtitle="Team Standup",
    icon=Path(__file__).parent / "zoom.png",
    action_button_str="Join zoom meeting",
    action_button_callback=partial(join_zoom_meeting, conf_number=zoom_conf_number)
)
```

##  Why did you create this library?
I wanted a library that did not depend on any non-python tools (so you had to go around and install that). Instead, I wanted a library where you install the pip packages, and you are done.
Later I realised how hard it was to integrate correctly with PyOBJC. Also, I had a hard time finding any examples on how to easily integrate this in a non-blocking fashion with my tool. 
Hence, I figured I should set it up to be as user-friendly as possible and share it with the world ;)!


## Limitations
Although there are some limitations, there is no reason to not use it now :v:.
- You need to keep your application running while waiting for the callback to happen.
- Currently, we are only supporting the old deprecated [user notifications](https://developer.apple.com/documentation/foundation/nsusernotification). Soon we will also make the new implementation available.
