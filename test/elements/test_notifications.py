import unittest

import requests_mock

from grafana_client import GrafanaApi


class NotificationsTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_channels(self, mock):
        mock.get(
            "http://localhost/api/alert-notifications",
            json=[
                {
                    "id": 1,
                    "uid": "team-a-email-notifier",
                    "name": "Team A",
                    "type": "email",
                    "isDefault": False,
                    "sendReminder": False,
                    "disableResolveMessage": False,
                    "settings": {"addresses": "dev@grafana.com"},
                    "created": "2018-04-23T14:44:09+02:00",
                    "updated": "2018-08-20T15:47:49+02:00",
                }
            ],
        )
        notification_channels = self.grafana.notifications.get_channels()
        self.assertEqual(len(notification_channels), 1)

        channel = notification_channels[0]
        self.assertEqual(channel["id"], 1)
        self.assertEqual(channel["uid"], "team-a-email-notifier")
        self.assertEqual(channel["name"], "Team A")
        self.assertEqual(channel["type"], "email")
        self.assertFalse(channel["isDefault"])
        self.assertFalse(channel["sendReminder"])
        self.assertFalse(channel["disableResolveMessage"])
        self.assertEqual(channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(channel["created"], "2018-04-23T14:44:09+02:00")
        self.assertEqual(channel["updated"], "2018-08-20T15:47:49+02:00")

    @requests_mock.Mocker()
    def test_lookup_channels(self, mock):
        mock.get(
            "http://localhost/api/alert-notifications/lookup",
            json=[
                {
                    "id": 1,
                    "uid": "000000001",
                    "name": "Test",
                    "type": "email",
                    "isDefault": False,
                },
                {
                    "id": 2,
                    "uid": "000000002",
                    "name": "Slack",
                    "type": "slack",
                    "isDefault": False,
                },
            ],
        )
        notification_channels = self.grafana.notifications.lookup_channels()
        self.assertEqual(len(notification_channels), 2)

        channel_1 = notification_channels[0]
        self.assertEqual(channel_1["id"], 1)
        self.assertEqual(channel_1["uid"], "000000001")
        self.assertEqual(channel_1["name"], "Test")
        self.assertEqual(channel_1["type"], "email")
        self.assertFalse(channel_1["isDefault"])

        channel_2 = notification_channels[1]
        self.assertEqual(channel_2["id"], 2)
        self.assertEqual(channel_2["uid"], "000000002")
        self.assertEqual(channel_2["name"], "Slack")
        self.assertEqual(channel_2["type"], "slack")
        self.assertFalse(channel_2["isDefault"])

    @requests_mock.Mocker()
    def test_get_channel_by_uid(self, mock):
        mock.get(
            "http://localhost/api/alert-notifications/uid/team-a-email-notifier",
            json={
                "id": 1,
                "uid": "team-a-email-notifier",
                "name": "Team A",
                "type": "email",
                "isDefault": False,
                "sendReminder": False,
                "disableResolveMessage": False,
                "settings": {"addresses": "dev@grafana.com"},
                "created": "2018-04-23T14:44:09+02:00",
                "updated": "2018-08-20T15:47:49+02:00",
            },
        )

        channel = self.grafana.notifications.get_channel_by_uid("team-a-email-notifier")
        self.assertEqual(channel["id"], 1)
        self.assertEqual(channel["uid"], "team-a-email-notifier")
        self.assertEqual(channel["name"], "Team A")
        self.assertEqual(channel["type"], "email")
        self.assertFalse(channel["isDefault"])
        self.assertFalse(channel["sendReminder"])
        self.assertFalse(channel["disableResolveMessage"])
        self.assertEqual(channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(channel["created"], "2018-04-23T14:44:09+02:00")
        self.assertEqual(channel["updated"], "2018-08-20T15:47:49+02:00")

    @requests_mock.Mocker()
    def test_get_channel_by_id(self, mock):
        mock.get(
            "http://localhost/api/alert-notifications/1",
            json={
                "id": 1,
                "uid": "team-a-email-notifier",
                "name": "Team A",
                "type": "email",
                "isDefault": False,
                "sendReminder": False,
                "disableResolveMessage": False,
                "settings": {"addresses": "dev@grafana.com"},
                "created": "2018-04-23T14:44:09+02:00",
                "updated": "2018-08-20T15:47:49+02:00",
            },
        )

        channel = self.grafana.notifications.get_channel_by_id(1)
        self.assertEqual(channel["id"], 1)
        self.assertEqual(channel["uid"], "team-a-email-notifier")
        self.assertEqual(channel["name"], "Team A")
        self.assertEqual(channel["type"], "email")
        self.assertFalse(channel["isDefault"])
        self.assertFalse(channel["sendReminder"])
        self.assertFalse(channel["disableResolveMessage"])
        self.assertEqual(channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(channel["created"], "2018-04-23T14:44:09+02:00")
        self.assertEqual(channel["updated"], "2018-08-20T15:47:49+02:00")

    @requests_mock.Mocker()
    def test_create_channel(self, mock):
        mock.post(
            "http://localhost/api/alert-notifications",
            json={
                "id": 2,
                "uid": "new-alert-notification",
                "name": "new alert notification",
                "type": "email",
                "isDefault": False,
                "sendReminder": False,
                "disableResolveMessage": False,
                "settings": {"addresses": "dev@grafana.com"},
                "created": "2018-04-23T14:44:09+02:00",
                "updated": "2018-08-20T15:47:49+02:00",
            },
        )

        payload = {
            "uid": "new-alert-notification",
            "name": "new alert notification",
            "type": "email",
            "isDefault": False,
            "sendReminder": False,
            "settings": {"addresses": "dev@grafana.com"},
        }

        created_channel = self.grafana.notifications.create_channel(payload)
        self.assertEqual(created_channel["id"], 2)
        self.assertEqual(created_channel["uid"], "new-alert-notification")
        self.assertEqual(created_channel["name"], "new alert notification")
        self.assertEqual(created_channel["type"], "email")
        self.assertFalse(created_channel["isDefault"])
        self.assertFalse(created_channel["sendReminder"])
        self.assertFalse(created_channel["disableResolveMessage"])
        self.assertEqual(created_channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(created_channel["created"], "2018-04-23T14:44:09+02:00")
        self.assertEqual(created_channel["updated"], "2018-08-20T15:47:49+02:00")

    @requests_mock.Mocker()
    def test_update_channel_by_uid(self, mock):
        mock.put(
            "http://localhost/api/alert-notifications/uid/new-alert-notification",
            json={
                "id": 1,
                "uid": "new-alert-notification",
                "name": "new alert notification",
                "type": "email",
                "isDefault": False,
                "sendReminder": True,
                "frequency": "15m",
                "settings": {"addresses": "dev@grafana.com"},
                "created": "2017-01-01 12:34",
                "updated": "2020-01-01 12:34",
            },
        )

        payload = {
            "uid": "new-alert-notification",
            "name": "new alert notification",
            "type": "email",
            "isDefault": False,
            "sendReminder": True,
            "frequency": "15m",
            "settings": {"addresses": "dev@grafana.com"},
        }

        updated_channel = self.grafana.notifications.update_channel_by_uid("new-alert-notification", payload)
        self.assertEqual(updated_channel["id"], 1)
        self.assertEqual(updated_channel["uid"], "new-alert-notification")
        self.assertEqual(updated_channel["name"], "new alert notification")
        self.assertEqual(updated_channel["type"], "email")
        self.assertFalse(updated_channel["isDefault"])
        self.assertTrue(updated_channel["sendReminder"])
        self.assertEqual(updated_channel["frequency"], "15m")
        self.assertEqual(updated_channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(updated_channel["created"], "2017-01-01 12:34")
        self.assertEqual(updated_channel["updated"], "2020-01-01 12:34")

    @requests_mock.Mocker()
    def test_update_channel_by_id(self, mock):
        mock.put(
            "http://localhost/api/alert-notifications/1",
            json={
                "id": 1,
                "uid": "new-alert-notification",
                "name": "new alert notification",
                "type": "email",
                "isDefault": False,
                "sendReminder": True,
                "frequency": "15m",
                "settings": {"addresses": "dev@grafana.com"},
                "created": "2017-01-01 12:34",
                "updated": "2020-01-01 12:34",
            },
        )

        payload = {
            "uid": "new-alert-notification",
            "name": "new alert notification",
            "type": "email",
            "isDefault": False,
            "sendReminder": True,
            "frequency": "15m",
            "settings": {"addresses": "dev@grafana.com"},
        }

        updated_channel = self.grafana.notifications.update_channel_by_id(1, payload)
        self.assertEqual(updated_channel["id"], 1)
        self.assertEqual(updated_channel["uid"], "new-alert-notification")
        self.assertEqual(updated_channel["name"], "new alert notification")
        self.assertEqual(updated_channel["type"], "email")
        self.assertFalse(updated_channel["isDefault"])
        self.assertTrue(updated_channel["sendReminder"])
        self.assertEqual(updated_channel["frequency"], "15m")
        self.assertEqual(updated_channel["settings"]["addresses"], "dev@grafana.com")
        self.assertEqual(updated_channel["created"], "2017-01-01 12:34")
        self.assertEqual(updated_channel["updated"], "2020-01-01 12:34")

    @requests_mock.Mocker()
    def test_delete_notification_by_uid(self, mock):
        mock.delete(
            "http://localhost/api/alert-notifications/uid/new-alert-notification",
            json={"message": "Notification deleted"},
        )

        delete_response = self.grafana.notifications.delete_notification_by_uid("new-alert-notification")
        self.assertEqual(delete_response["message"], "Notification deleted")

    @requests_mock.Mocker()
    def test_delete_notification_by_id(self, mock):
        mock.delete(
            "http://localhost/api/alert-notifications/1",
            json={"message": "Notification deleted"},
        )

        delete_response = self.grafana.notifications.delete_notification_by_id(1)
        self.assertEqual(delete_response["message"], "Notification deleted")
