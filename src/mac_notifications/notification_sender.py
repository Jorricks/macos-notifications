from multiprocessing import Queue
from typing import Any

from Foundation import NSUserNotification, NSUserNotificationCenter, NSObject, NSDate, NSURL
from AppKit import NSImage
from PyObjCTools import AppHelper

from mac_notifications.notification_config import JSONNotificationConfig


def send_notification(queue: Queue, config: JSONNotificationConfig) -> Any:
    class MacOSNotification(NSObject):
        def send(self):
            notification = NSUserNotification.alloc().init()
            print(config)

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

            if config.do_nothing_button_str:
                notification.setOtherButtonTitle_(config.do_nothing_button_str)

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
            if config.contains_callback:
                print('Started listening.')
                AppHelper.runConsoleEventLoop()

        def userNotificationCenter_shouldPresentNotification_(
            self,
            center: "_NSConcreteUserNotificationCenter",
            notif: "_NSConcreteUserNotification"
        ):
            print('Should present notification.')
            # print("center:", type(center), dir(center))
            # print("notif:", type(notif), dir(notif))

        def userNotificationCenter_didDeliverNotification_(
            self,
            center: "_NSConcreteUserNotificationCenter",
            notif: "_NSConcreteUserNotification"
        ):
            print('Delivered notification.')
            # print("center:", type(center), dir(center))
            # print("notif:", type(notif), dir(notif))

        def userNotificationCenter_didActivateNotification_(
            self,
            center: "_NSConcreteUserNotificationCenter",
            notif: "_NSConcreteUserNotification"
        ):
            response = notif.response()
            print('User interacted with the notification.')
            # print("center:", type(center), dir(center))
            # print("notif:", type(notif), dir(notif))
            # print("response:", type(response), response, dir(response))
            #
            # print(notif.activationType())

            if notif.activationType() == 1:
                # user clicked on the notification (not on a button)
                # don't stop event loop because the other buttons can still be pressed
                pass

            elif notif.activationType() == 2:
                # user clicked on the action button
                queue.put((config.uid, "action_button_clicked", ""), block=True, timeout=1.0)
                AppHelper.stopEventLoop()

            elif notif.activationType() == 3:
                # User clicked on the reply button
                reply_text = response.string()
                queue.put((config.uid, "reply_button_clicked", reply_text))
                AppHelper.stopEventLoop()

    # create the new notification
    new_notif = MacOSNotification.alloc().init()

    # return notification
    return new_notif
