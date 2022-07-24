from __future__ import annotations

import logging
from multiprocessing import SimpleQueue
from typing import Any

from AppKit import NSImage
from Foundation import NSDate, NSObject, NSURL, NSUserNotification, NSUserNotificationCenter
from PyObjCTools import AppHelper

from mac_notifications.notification_config import JSONNotificationConfig

logger = logging.getLogger()


def create_notification(queue: SimpleQueue, config: JSONNotificationConfig, listen: bool = False) -> Any:
    class MacOSNotification(NSObject):
        def send(self):
            """Sending of the notification"""
            notification = NSUserNotification.alloc().init()
            notification.setIdentifier_(config.uid)
            if config is not None:
                notification.setTitle_(config.title)
            if config.subtitle is not None:
                notification.setSubtitle_(config.subtitle)
            if config.text is not None:
                notification.setInformativeText_(config.text)
            if config.icon is not None:
                url = NSURL.alloc().initWithString_(f"file://{config.icon}")
                image = NSImage.alloc().initWithContentsOfURL_(url)
                notification.setContentImage_(image)
                # notification.set_contentImageData_()

            # Notification buttons (main action button and other button)
            if config.action_button_str:
                notification.setActionButtonTitle_(config.action_button_str)
                notification.setHasActionButton_(True)

            if config.snooze_button_str:
                notification.setOtherButtonTitle_(config.snooze_button_str)

            # Reply button
            if config.reply_callback_present:
                notification.setHasReplyButton_(True)
                if config.reply_button_str:
                    notification.setResponsePlaceholder_(config.reply_button_str)

            NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)

            # Setting delivery date as current date + delay (in seconds)
            notification.setDeliveryDate_(
                NSDate.dateWithTimeInterval_sinceDate_(config.delay_in_seconds, NSDate.date())
            )

            # Schedule the notification send
            NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

            # Wait for the notification CallBack to happen.
            if listen:
                logger.debug("Started listening for user interactions with notifications.")
                AppHelper.runConsoleEventLoop()

        def userNotificationCenter_didDeliverNotification_(
            self, center: "_NSConcreteUserNotificationCenter", notif: "_NSConcreteUserNotification"  # type: ignore
        ) -> None:
            """Respond to the delivering of the notification."""
            logger.debug(f"Delivered: {notif.identifier()}")

        def userNotificationCenter_didActivateNotification_(
            self, center: "_NSConcreteUserNotificationCenter", notif: "_NSConcreteUserNotification"  # type: ignore
        ) -> None:
            """
            Respond to a user interaction with the notification.
            """
            identifier = notif.identifier()
            response = notif.response()
            activation_type = notif.activationType()
            logger.debug(f"User interacted with {identifier} with activationType {activation_type}.")
            if activation_type == 1:
                # user clicked on the notification (not on a button)
                pass

            elif activation_type == 2:  # user clicked on the action button
                queue.put((identifier, "action_button_clicked", ""))

            elif activation_type == 3:  # User clicked on the reply button
                queue.put((identifier, "reply_button_clicked", response.string()))

    # create the new notification
    new_notif = MacOSNotification.alloc().init()

    # return notification
    return new_notif