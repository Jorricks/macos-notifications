"""
This module is responsible for creating the notifications in the C-layer and listening/reporting about user activity.
"""
from __future__ import annotations

import logging
import re
from multiprocessing import SimpleQueue
from typing import Any, Type

import ctypes
from AppKit import NSImage
from Foundation import NSDate, NSObject, NSURL, NSUserNotification, NSUserNotificationCenter
from objc import python_method
from PyObjCTools import AppHelper

from mac_notifications.notification_config import JSONNotificationConfig

logger = logging.getLogger()


def create_notification(config: JSONNotificationConfig, queue_to_submit_events_to: SimpleQueue | None) -> None:
    """
    Create a notification and possibly listen & report about notification activity.
    :param config: The configuration of the notification to send.
    :param queue_to_submit_events_to: The Queue to submit user activity related to the callbacks to. If this argument
    is passed, it will start the event listener after it created the Notifications. If this is None, it will only
    create the notification.
    """
    notification = _build_notification(config)
    macos_notification = MacOSNotification.alloc().init()
    macos_notification.send(notification, config, queue_to_submit_events_to)


class MacOSNotification(NSObject):
    @python_method
    def send(
            self,
            notification: NSUserNotification,
            config: JSONNotificationConfig,
            queue_to_submit_events_to: SimpleQueue | None
        ):
        """Sending of the notification"""
        self.queue_to_submit_events_to = queue_to_submit_events_to
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)

        # Setting delivery date as current date + delay (in seconds)
        notification.setDeliveryDate_(
            NSDate.dateWithTimeInterval_sinceDate_(config.delay_in_seconds, NSDate.date())
        )

        # Schedule the notification send
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

        # Wait for the notification CallBack to happen.
        if queue_to_submit_events_to:
            logger.debug("Started listening for user interactions with notifications.")
            AppHelper.runConsoleEventLoop()

    def userNotificationCenter_didDeliverNotification_(
            self,
            center: "_NSConcreteUserNotificationCenter",
            notif: "_NSConcreteUserNotification"
    ) -> None:
        """Respond to the delivering of the notification."""
        logger.debug(f"Delivered: {notif.identifier()}")

    def userNotificationCenter_didActivateNotification_(
            self,
            center: "_NSConcreteUserNotificationCenter",
            notif: "_NSConcreteUserNotification"  # type: ignore  # noqa
    ) -> None:
        """
        Respond to a user interaction with the notification.
        """
        identifier = notif.identifier()
        response = notif.response()
        activation_type = notif.activationType()

        if self.queue_to_submit_events_to is None:
            raise ValueError("Queue should not be None here.")
        else:
            queue: SimpleQueue = self.queue_to_submit_events_to

        logger.debug(f"User interacted with {identifier} with activationType {activation_type}.")
        if activation_type == 1:
            # user clicked on the notification (not on a button)
            pass

        elif activation_type == 2:  # user clicked on the action button
            queue.put((identifier, "action_button_clicked", ""))

        elif activation_type == 3:  # User clicked on the reply button
            queue.put((identifier, "reply_button_clicked", response.string()))


def cancel_notification(uid:str) -> None:
    notification = NSUserNotification.alloc().init()
    notification.setIdentifier_(uid)
    NSUserNotificationCenter.defaultUserNotificationCenter().removeDeliveredNotification_(notification)


def _build_notification(config: JSONNotificationConfig) -> NSUserNotification:
    notification = NSUserNotification.alloc().init()
    notification.setIdentifier_(config.uid)
    if config is not None:
        notification.setTitle_(config.title)
    if config.subtitle is not None:
        notification.setSubtitle_(config.subtitle)
    if config.text is not None:
        notification.setInformativeText_(config.text)
    if config.sound is not None:
        notification.setSoundName_(config.sound)
    if config.icon is not None:
        url = NSURL.alloc().initWithString_(f"file://{config.icon}")
        image = NSImage.alloc().initWithContentsOfURL_(url)
        notification.setContentImage_(image)

    # Notification buttons (main action button and other button)
    if config.action_button_str:
        notification.setActionButtonTitle_(config.action_button_str)
        notification.setHasActionButton_(True)

    if config.snooze_button_str:
        notification.setOtherButtonTitle_(config.snooze_button_str)

    if config.reply_callback_present:
        notification.setHasReplyButton_(True)
        if config.reply_button_str:
            notification.setResponsePlaceholder_(config.reply_button_str)

    return notification


# Hardcore way to dealloc an Objective-C class from https://github.com/albertz/chromehacking/blob/master/disposeClass.py
def dispose_of_objc_class(cls: Type):
    """Deallocate an objective C class (del cls does not remove the class from memory)."""
    address = int(re.search("0x[0-9a-f]+", repr(cls)).group(0), 16)
    logger.info(f"Disposing of class '{cls.__name__}' at addr: {hex(address)}")
    print(f"Disposing of class '{cls.__name__}' at addr: {hex(address)}")
    ctypes.pythonapi.objc_disposeClassPair.restype = None
    ctypes.pythonapi.objc_disposeClassPair.argtypes = (ctypes.c_void_p,)
    ctypes.pythonapi.objc_disposeClassPair(address)
