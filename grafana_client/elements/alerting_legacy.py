"""
Legacy Alerting API.
Legacy Alerting Notification Channels API.

Starting with v9.0, the Legacy Alerting (Notification Channels) APIs are deprecated.
They have been removed with Grafana 11.

https://grafana.com/docs/grafana/v10.0/developers/http_api/alerting/
https://grafana.com/docs/grafana/v10.0/developers/http_api/alerting_notification_channels/
"""

# pragma: exclude file

import warnings

from .base import Base


def emit_deprecation_warning():
    warnings.warn(
        "The Legacy Alerting (Notification Channels) APIs were deprecated with Grafana 9 and removed with Grafana 11.",
        DeprecationWarning,
    )


class Alerting(Base):
    def __init__(self, client):
        super(Alerting, self).__init__(client)
        self.client = client

    def get_alertrule(self, folder_name, alertrule_name):
        """
        :param folder_name:
        :param alertrule_name:
        :return:
        """
        emit_deprecation_warning()
        get_alertrule_path = "/ruler/grafana/api/v1/rules/%s/%s" % (folder_name, alertrule_name)
        return self.client.GET(get_alertrule_path)

    def get_managedalerts_all(self, datasource="grafanacloud-prom"):
        """ """
        emit_deprecation_warning()
        get_managedalerts_path = "/prometheus/%s/api/v1/rules" % datasource
        return self.client.GET(get_managedalerts_path)

    def create_alertrule(self, folder_name, alertrule):
        """
        :param folder_name:
        :param alertrule:
        :return:
        """
        emit_deprecation_warning()
        create_alertrule_path = "/ruler/grafana/api/v1/rules/%s" % folder_name
        return self.client.POST(create_alertrule_path, json=alertrule)

    def update_alertrule(self, folder_name, alertrule):
        """
        @param folder_name:
        @param alertrule:
        @return:
        """
        emit_deprecation_warning()
        update_alertrule_path = "/ruler/grafana/api/v1/rules/%s" % folder_name
        return self.client.POST(update_alertrule_path, json=alertrule)

    def delete_alertrule(self, folder_name, alertrule_name):
        """
        :param folder_name:
        :param alertrule_name:
        @return:
        """
        emit_deprecation_warning()
        delete_alertrule_path = "/ruler/grafana/api/v1/rules/%s/%s" % (folder_name, alertrule_name)
        return self.client.DELETE(delete_alertrule_path)


class Notifications(Base):
    def __init__(self, client):
        super(Notifications, self).__init__(client)
        self.client = client

    def get_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels

        :return: all notification channels that the authenticated user has permission to view
        """
        emit_deprecation_warning()
        get_channels_path = "/alert-notifications"
        return self.client.GET(get_channels_path)

    def lookup_channels(self):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-all-notification-channels-lookup

        :return: all notification channels, but with less detailed information
        """
        emit_deprecation_warning()
        lookup_channels_path = "/alert-notifications/lookup"
        return self.client.GET(lookup_channels_path)

    def get_channel_by_uid(self, channel_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-uid

        :param channel_uid: notification channel uid
        :return: notification channel for the given channel uid
        """
        emit_deprecation_warning()
        get_channel_by_uid_path = "/alert-notifications/uid/%s" % channel_uid
        return self.client.GET(get_channel_by_uid_path)

    def get_channel_by_id(self, channel_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#get-notification-channel-by-id

        :param: notification channel id
        :return: notification channel for the given channel id
        """
        emit_deprecation_warning()
        get_channel_by_id_path = "/alert-notifications/%s" % channel_id
        return self.client.GET(get_channel_by_id_path)

    def create_channel(self, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#create-notification-channel

        :param: channel to be created
        :return: created channel
        """
        emit_deprecation_warning()
        create_channel_path = "/alert-notifications"
        return self.client.POST(create_channel_path, json=channel)

    def update_channel_by_uid(self, uid, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-uid

        :param uid: notification channel uid
        :param channel: updated version of channel
        :return: updated version of channel
        """
        emit_deprecation_warning()
        update_channel_by_uid_path = "/alert-notifications/uid/%s" % uid
        return self.client.PUT(update_channel_by_uid_path, json=channel)

    def update_channel_by_id(self, id, channel):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#update-notification-channel-by-id

        :param id: notification channel id
        :param channel: updated version of channel
        :return: updated version of channel
        """
        emit_deprecation_warning()
        update_channel_by_id_path = "/alert-notifications/%s" % id
        return self.client.PUT(update_channel_by_id_path, json=channel)

    def delete_notification_by_uid(self, notification_uid):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_uid: notification channel uid
        :return: result of deletion
        """
        emit_deprecation_warning()
        delete_notification_by_uid_path = "/alert-notifications/uid/%s" % notification_uid
        return self.client.DELETE(delete_notification_by_uid_path)

    def delete_notification_by_id(self, notification_id):
        """
        https://grafana.com/docs/grafana/latest/http_api/alerting_notification_channels/#delete-alert-notification-by-uid

        :param notification_id: notification channel id
        :return: result of deletion
        """
        emit_deprecation_warning()
        delete_notification_by_id_path = "/alert-notifications/%s" % notification_id
        return self.client.DELETE(delete_notification_by_id_path)
