# The client

When you are looking to integrate macos-notifications with your project, the `client` is the first place to look.
If you have a service that periodically restarts, you might want to take a look at the `CacheClient`.

::: mac_notifications.client


## More advanced usages
To get a bit more information about the amount of notifications that are still active, you can use the following function:

::: mac_notifications.client.get_notification_manager
