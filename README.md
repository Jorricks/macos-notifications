<p align="center">
  <a href="https://github.com/Jorricks/macos-notifications"><img src="https://github.com/Jorricks/macos-notifications/raw/main/docs/img/macos-notifications.png" alt="macos-notifications" width="600px"></a>
</p>
<p align="center">
<a href="https://www.apple.com/mac/" target="_blank">
    <img src="https://img.shields.io/badge/Platform-mac-blue" alt="Mac supported">
</a>
<a href="https://pypi.org/project/macos-notifications" target="_blank">
    <img src="https://img.shields.io/pypi/v/macos-notifications?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/macos-notifications" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/macos-notifications.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://jorricks.github.io/macos-notifications/](https://jorricks.github.io/macos-notifications/)

**Source Code**: [https://github.com/Jorricks/macos-notifications](https://github.com/Jorricks/macos-notifications)

---

**mac-notification** is a Python library to make it as easy as possible to create interactable notifications.


## Installation

To use macos-notifications, first install it using pip:

    pip install macos-notifications


## Features
- 🚀 Easy python interface. It's as simple as '`client.create_notification(title="Meeting starts now!", subtitle="Team Standup")`'
- 💥 Ability to add action buttons with callbacks!
- 📝 Ability to reply to notifications!
- ⌚ Delayed notifications.
- ⏱️ Automatically time out the notification listener.
- 📦 Just `pyobjc` as a dependency.

## Example
```python
from functools import partial
from mac_notifications import client

if __name__ == "__main__":
    client.create_notification(
        title="Meeting starts now!",
        subtitle="Team Standup",
        icon="/Users/jorrick/zoom.png",
        sound="Frog",
        action_button_str="Join zoom meeting",
        action_callback=partial(join_zoom_meeting, conf_number=zoom_conf_number)
    )
```
A simple example. Please look [in the docs](https://jorricks.github.io/macos-notifications/) for more examples like this:

<p align="center">
<a href="https://jorricks.github.io/macos-notifications/examples/">
<img src="https://github.com/Jorricks/macos-notifications/raw/main/docs/img/example-run.gif" alt="macos-notifications" width="600px">
</a>
</p>

##  Why did you create this library?
I wanted a library that did not depend on any non-python tools (so you had to go around and install that). Instead, I wanted a library where you install the pip packages, and you are done.
Later I realised how hard it was to integrate correctly with PyOBJC. Also, I had a hard time finding any examples on how to easily integrate this in a non-blocking fashion with my tool.
Hence, I figured I should set it up to be as user-friendly as possible and share it with the world ;)!


## Limitations
Although there are some limitations, there is no reason to not use it now :v:.
- You need to keep your application running while waiting for the callback to happen.
- We do not support raising notifications from anything but the main thread. If you wish to raise it from other threads, you need to set up a communication channel with the main thread, which in turn than raises the notification.
- Currently, we are only supporting the old deprecated [user notifications](https://developer.apple.com/documentation/foundation/nsusernotification). If you wish to use the new implementation, please feel free to propose an MR.
- You can not change the main image of the notification to be project specific. You can only change the Python interpreter image, but that would impact all notifications send by Python.
