from ..base import Base


class Notifications(Base):
    def __init__(self, client):
        super(Notifications, self).__init__(client)
        self.client = client

    async def get_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels

        :return: all notification channels that the authenticated user has permission to view
        """
        get_channels_path = "/alert-notifications"
        return await self.client.GET(get_channels_path)

    async def lookup_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels-lookup

        :return: all notification channels, but with less detailed information
        """
        lookup_channels_path = "/alert-notifications/lookup"
        return await self.client.GET(lookup_channels_path)

    async def get_channel_by_uid(self, channel_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-uid

        :param channel_uid: notification channel uid
        :return: notification channel for the given channel uid
        """
        get_channel_by_uid_path = "/alert-notifications/uid/%s" % channel_uid
        return await self.client.GET(get_channel_by_uid_path)

    async def get_channel_by_id(self, channel_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-id

        :param: notification channel id
        :return: notification channel for the given channel id
        """
        get_channel_by_id_path = "/alert-notifications/%s" % channel_id
        return await self.client.GET(get_channel_by_id_path)

    async def create_channel(self, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#create-notification-channel

        :param: channel to be created
        :return: created channel
        """
        create_channel_path = "/alert-notifications"
        return await self.client.POST(create_channel_path, json=channel)

    async def update_channel_by_uid(self, uid, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-uid

        :param uid: notification channel uid
        :param channel: updated version of channel
        :return: updated version of channel
        """
        update_channel_by_uid_path = "/alert-notifications/uid/%s" % uid
        return await self.client.PUT(update_channel_by_uid_path, json=channel)

    async def update_channel_by_id(self, id, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-id

        :param id: notification channel id
        :param channel: updated version of channel
        :return: updated version of channel
        """
        update_channel_by_id_path = "/alert-notifications/%s" % id
        return await self.client.PUT(update_channel_by_id_path, json=channel)

    async def delete_notification_by_uid(self, notification_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_uid: notification channel uid
        :return: result of deletion
        """
        delete_notification_by_uid_path = "/alert-notifications/uid/%s" % notification_uid
        return await self.client.DELETE(delete_notification_by_uid_path)

    async def delete_notification_by_id(self, notification_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_id: notification channel id
        :return: result of deletion
        """
        delete_notification_by_id_path = "/alert-notifications/%s" % notification_id
        return await self.client.DELETE(delete_notification_by_id_path)
