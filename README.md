<p align="center">
  <a href="https://github.com/Jorricks/mac-notifications"><img src="https://github.com/Jorricks/mac-notifications/raw/main/docs/mac-notifications.png" alt="mac-notifications" width="600px"></a>
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

**Documentation**: [https://jorricks.github.io/mac-notifications/](https://jorricks.github.io/mac-notifications/)

**Source Code**: [https://github.com/Jorricks/mac-notifications](https://github.com/Jorricks/mac-notifications)

---

**mac-notification** is a Python library to make it as easy as possible to create interactable notifications.

## Features
- 🚀 Easy python interface. It's as simple as '`client.create_notification(title="Meeting starts now!", subtitle="Team Standup")`'
- 💥 Ability to add action buttons.
- 📝 Ability to reply to the notification.
- ⌚ Delayed notifications.
- ⏱️ Automatically time out the notification listener.
- 📦 Just two packages (which is really just one package) as a dependency


## Installation

To use mac-notifications, first install it using pip:

    pip install mac-notifications

## Requirements
Python 3.8+

mac-notifications uses two major libraries for their date and time utilities:
- [Pendulum](https://github.com/sdispater/pendulum) for its extensions on datetime objects and parsing of durations.
- [Python-Dateutil](https://github.com/dateutil/dateutil) for its RRule support.


## Installation

To use mac-notifications, first install it using pip:

    pip install mac-notifications

## Requirements
Python 3.8+

Mac-notification only relies on `pyobjc`:
- The [PyObjC project](https://pyobjc.readthedocs.io/) aims to provide a bridge between the Python and Objective-C programming languages on macOS.

## Example
A simple example. Please look [in the docs](https://jorricks.github.io/mac-notifications/) for more examples.

```python

client.create_notification(
    title="Meeting starts now!",
    subtitle="Team Standup",
    icon="/Users/jorrick/zoom.png",
    action_button_str="Join zoom meeting",
    action_button_callback=partial(join_zoom_meeting, conf_number=zoom_conf_number)
)
```

##  Why did you create this library?
I wanted a library that did not depend on any non-python tools (so you had to go around and install that), I wanted a library where you install the pip packages, and you are done.
Later I realised how hard it was to integrate correctly with PyOBJC. Also, I had a hard time finding any examples on how to easily integrate this in a non-blocking fashion with my tool. 
Hence, I figured I should set it up to be as user-friendly as possible and share it with the world ;)!


## Limitations
Although there are some limitations, there is no reason to not use it now :v:.
- When you close a notification, it is possible the Python application does not get this command (This is a limitation of `pyobjc`). Therefor, to prevent it from waiting endlessly, you should define a `callback_timeout`!
- You need to keep your application running while waiting for the callback to happen.
- Currently, we are only supporting the old deprecated [user notifications](https://developer.apple.com/documentation/foundation/nsusernotification). Soon we will also make the new implementation available.
