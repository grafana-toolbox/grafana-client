from .base import Base


class Notifications(Base):
    def __init__(self, client):
        super(Notifications, self).__init__(client)
        self.client = client

    def get_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels

        :return: all notification channels that the authenticated user has permission to view
        """
        get_channels_path = "/alert-notifications"
        return self.client.GET(get_channels_path)

    def lookup_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels-lookup

        :return: all notification channels, but with less detailed information
        """
        lookup_channels_path = "/alert-notifications/lookup"
        return self.client.GET(lookup_channels_path)

    def get_channel_by_uid(self, channel_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-uid

        :param channel_uid: notification channel uid
        :return: notification channel for the given channel uid
        """
        get_channel_by_uid_path = "/alert-notifications/uid/%s" % channel_uid
        return self.client.GET(get_channel_by_uid_path)

    def get_channel_by_id(self, channel_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-id

        :param: notification channel id
        :return: notification channel for the given channel id
        """
        get_channel_by_id_path = "/alert-notifications/%s" % channel_id
        return self.client.GET(get_channel_by_id_path)

    def create_channel(self, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#create-notification-channel

        :param: channel to be created
        :return: created channel
        """
        create_channel_path = "/alert-notifications"
        return self.client.POST(create_channel_path, json=channel)

    def update_channel_by_uid(self, uid, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-uid

        :param uid: notification channel uid
        :param channel: updated version of channel
        :return: updated version of channel
        """
        update_channel_by_uid_path = "/alert-notifications/uid/%s" % uid
        return self.client.PUT(update_channel_by_uid_path, json=channel)

    def update_channel_by_id(self, id, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-id

        :param id: notification channel id
        :param channel: updated version of channel
        :return: updated version of channel
        """
        update_channel_by_id_path = "/alert-notifications/%s" % id
        return self.client.PUT(update_channel_by_id_path, json=channel)

    def delete_notification_by_uid(self, notification_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_uid: notification channel uid
        :return: result of deletion
        """
        delete_notification_by_uid_path = "/alert-notifications/uid/%s" % notification_uid
        return self.client.DELETE(delete_notification_by_uid_path)

    def delete_notification_by_id(self, notification_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_id: notification channel id
        :return: result of deletion
        """
        delete_notification_by_id_path = "/alert-notifications/%s" % notification_id
        return self.client.DELETE(delete_notification_by_id_path)
