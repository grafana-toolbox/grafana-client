"""
Legacy Alerting API.
Legacy Alerting Notification Channels API.

Starting with v9.0, the Legacy Alerting (Notification Channels) APIs are deprecated.
They have been removed with Grafana 11.

https://grafana.com/docs/grafana/v10.0/developers/http_api/alerting/
https://grafana.com/docs/grafana/v10.0/developers/http_api/alerting_notification_channels/
"""

import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client.client import GrafanaBadInputError, GrafanaClientError, GrafanaServerError

ALERTRULE = {
    "name": "alert-rule-test",
    "id": 2,
    "uid": "bUUGqLiVk",
    "orgID": 1,
    "folderUID": "4",
    "ruleGroup": "Any",
    "title": "ApiAlerts",
    "condition": "B",
    "data": [],
    "updated": "2022-08-17T13:00:21Z",
    "noDataState": "NoData",
    "execErrState": "Alerting",
    "for": 300000000000,
    "labels": {"alertGroup": "any", "region": "eu-west-1"},
}

NOTIFICATION = {
    "uid": "team-a-email-notifier",
    "name": "Team A",
    "type": "email",
    "isDefault": False,
    "sendReminder": False,
    "settings": {"addresses": "dev@grafana.com"},
}


pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class AlertingTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api, reset_folders_dashboards):  # noqa: ARG002
        self.grafana = grafana_api
        if self.grafana.get_version() < Version("8"):
            pytest.skip("Alert rules: Not supported on Grafana 7 and earlier.")

        if self.grafana.get_version() >= Version("10.4"):
            pytest.skip("Legacy Alerting has been removed with Grafana 10.4.")

        self.folder = self.grafana.folder.create_folder("alert-folder")
        self.grafana.alerting.create_alertrule("alert-folder", alertrule=ALERTRULE)

    def test_get_alertrule(self):
        response = self.grafana.alerting.get_alertrule("alert-folder", "alert-rule-test")
        self.assertEqual(response["name"], "alert-rule-test")

    @pytest.mark.skip("Only applicable on Grafana Cloud")
    def test_get_managedalerts_all(self):
        """
        This test uses `grafanacloud-prom`. It is not applicable on standalone Grafana.

        URL: http://localhost/api/prometheus/grafanacloud-prom/api/v1/rules
        json: {"status": "success", "data": {"groups": []}}
        """
        response = self.grafana.alerting.get_managedalerts_all()
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["data"]["groups"], [])

    def test_delete_alertrule(self):
        response = self.grafana.alerting.delete_alertrule("alert-folder", "alert-rule-test")
        self.assertEqual(response["message"], "rules deleted")

    def test_create_alertrule(self):
        pass

    def test_update_alertrule(self):
        response = self.grafana.alerting.update_alertrule("alert-folder", alertrule=ALERTRULE)
        self.assertEqual(response["message"], "no changes detected in the rule group")


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class NotificationsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api):
        self.grafana = grafana_api

        if self.grafana.get_version() >= Version("11"):
            pytest.skip("Legacy Alerting Notification Channels have been removed with Grafana 11.")

        # Prune all channels.
        for channel in self.grafana.notifications.get_channels():
            self.grafana.notifications.delete_notification_by_id(channel["id"])

        # Provision single channel.
        self.channel = self.grafana.notifications.create_channel(NOTIFICATION)
        self.channel_uid = self.channel["uid"]
        self.channel_id = self.channel["id"]

    def test_get_channels(self):
        notification_channels = self.grafana.notifications.get_channels()
        self.assertEqual(len(notification_channels), 1)
        channel = notification_channels[0]
        self.assertEqual(channel["uid"], "team-a-email-notifier")
        self.assertEqual(channel["name"], "Team A")
        self.assertEqual(channel["type"], "email")
        self.assertFalse(channel["isDefault"])
        self.assertFalse(channel["sendReminder"])
        self.assertFalse(channel["disableResolveMessage"])
        self.assertEqual(channel["settings"]["addresses"], "dev@grafana.com")

    def test_lookup_channels(self):
        notification_channels = self.grafana.notifications.lookup_channels()
        self.assertEqual(len(notification_channels), 1)
        channel_1 = notification_channels[0]
        self.assertEqual(channel_1["uid"], "team-a-email-notifier")

    def test_get_channel_by_uid(self):
        channel = self.grafana.notifications.get_channel_by_uid("team-a-email-notifier")
        self.assertEqual(channel["uid"], "team-a-email-notifier")
        self.assertEqual(channel["name"], "Team A")
        self.assertEqual(channel["type"], "email")
        self.assertFalse(channel["isDefault"])
        self.assertFalse(channel["sendReminder"])
        self.assertFalse(channel["disableResolveMessage"])
        self.assertEqual(channel["settings"]["addresses"], "dev@grafana.com")

    def test_get_channel_by_id(self):
        channel = self.grafana.notifications.get_channel_by_id(self.channel_id)
        self.assertEqual(channel["id"], self.channel_id)
        self.assertEqual(channel["uid"], self.channel_uid)

    def test_create_channel_no_name(self):
        with self.assertRaises((GrafanaBadInputError, GrafanaClientError)) as context:
            self.grafana.notifications.create_channel({"type": "email"})
        self.assertIn(context.exception.status_code, [400, 422])
        self.assertRegex(str(context.exception), "(bad request data|RequiredError)")

    def test_create_channel_no_type(self):
        with self.assertRaises((GrafanaBadInputError, GrafanaClientError)) as context:
            self.grafana.notifications.create_channel({"name": "42"})
        self.assertIn(context.exception.status_code, [400, 422])
        self.assertRegex(str(context.exception), "(bad request data|RequiredError)")

    def test_create_channel_no_addresses_in_settings(self):
        if self.grafana.get_version() < Version("8"):
            pytest.skip("Grafana 7 allows empty addresses in settings.")
        with self.assertRaises(GrafanaBadInputError) as context:
            self.grafana.notifications.create_channel({"name": "42", "type": "email", "settings": {}})
        self.assertIn(context.exception.status_code, [400, 422])
        self.assertIn("Could not find addresses in settings", str(context.exception))

    def test_create_channel_duplicate(self):
        def probe():
            self.grafana.notifications.create_channel(NOTIFICATION)

        if self.grafana.get_version() >= Version("7"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(context.exception.status_code, 409)
            self.assertIn("Failed to create alert notification", str(context.exception))
        else:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(context.exception.status_code, 500)
            self.assertIn("Failed to create alert notification", str(context.exception))

    def test_update_channel_by_uid(self):
        payload = {
            "uid": self.channel_uid,
            "name": "new alert notification",
            "type": "email",
            "isDefault": False,
            "sendReminder": True,
            "frequency": "15m",
            "settings": {"addresses": "dev@grafana.com"},
        }

        updated_channel = self.grafana.notifications.update_channel_by_uid(self.channel_uid, payload)
        self.assertEqual(updated_channel["id"], self.channel_id)
        self.assertEqual(updated_channel["uid"], self.channel_uid)
        self.assertEqual(updated_channel["name"], "new alert notification")
        self.assertEqual(updated_channel["type"], "email")
        self.assertFalse(updated_channel["isDefault"])
        self.assertTrue(updated_channel["sendReminder"])
        self.assertEqual(updated_channel["frequency"], "15m")
        self.assertEqual(updated_channel["settings"]["addresses"], "dev@grafana.com")

    def test_update_channel_by_id(self):

        payload = {
            "id": self.channel_id,
            "name": "new alert notification",
            "type": "email",
            "isDefault": False,
            "sendReminder": True,
            "frequency": "15m",
            "settings": {"addresses": "dev@grafana.com"},
        }

        updated_channel = self.grafana.notifications.update_channel_by_id(self.channel_id, payload)
        self.assertEqual(updated_channel["id"], self.channel_id)
        self.assertEqual(updated_channel["uid"], self.channel_uid)
        self.assertEqual(updated_channel["name"], "new alert notification")
        self.assertEqual(updated_channel["type"], "email")
        self.assertFalse(updated_channel["isDefault"])
        self.assertTrue(updated_channel["sendReminder"])
        self.assertEqual(updated_channel["frequency"], "15m")
        self.assertEqual(updated_channel["settings"]["addresses"], "dev@grafana.com")

    def test_delete_notification_by_uid(self):
        delete_response = self.grafana.notifications.delete_notification_by_uid(self.channel_uid)
        self.assertEqual(delete_response["message"], "Notification deleted")

    def test_delete_notification_by_id(self):
        delete_response = self.grafana.notifications.delete_notification_by_id(self.channel_id)
        self.assertEqual(delete_response["message"], "Notification deleted")
