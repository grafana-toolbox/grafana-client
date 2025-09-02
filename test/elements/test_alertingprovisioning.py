import unittest

from grafana_client import GrafanaApi

from ..compat import requests_mock

ALERTRULE = {
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


class AlertingProvisioningTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_alertrules_all(self, m):
        m.get(
            "http://localhost/api/v1/provisioning/alert-rules",
            json=[ALERTRULE],
        )
        response = self.grafana.alertingprovisioning.get_alertrules_all()
        self.assertEqual(response[0]["uid"], "bUUGqLiVk")

    @requests_mock.Mocker()
    def test_get_alertrule(self, m):
        m.get(
            "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
            json=ALERTRULE,
        )
        response = self.grafana.alertingprovisioning.get_alertrule("bUUGqLiVk")
        self.assertEqual(response["uid"], "bUUGqLiVk")

    @requests_mock.Mocker()
    def test_delete_alertrule(self, m):
        m.delete(
            "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
            json={"uid": "bUUGqLiVk"},
        )
        response = self.grafana.alertingprovisioning.delete_alertrule("bUUGqLiVk")
        self.assertEqual(response["uid"], "bUUGqLiVk")

    @requests_mock.Mocker()
    def test_create_alertrule_default(self, m):
        m.post(
            "http://localhost/api/v1/provisioning/alert-rules",
            json=ALERTRULE,
        )

        response = self.grafana.alertingprovisioning.create_alertrule(ALERTRULE)
        self.assertEqual(response["uid"], "bUUGqLiVk")

        # Verify request header.
        history = m.request_history
        headers = history[0].headers
        self.assertNotIn("X-Disable-Provenance", headers)

    @requests_mock.Mocker()
    def test_create_alertrule_disable_provenance(self, m):
        m.post(
            "http://localhost/api/v1/provisioning/alert-rules",
            json=ALERTRULE,
        )

        response = self.grafana.alertingprovisioning.create_alertrule(ALERTRULE, disable_provenance=True)
        self.assertEqual(response["uid"], "bUUGqLiVk")

        # Verify request header.
        history = m.request_history
        headers = history[0].headers
        self.assertIn("X-Disable-Provenance", headers)
        self.assertEqual(headers["X-Disable-Provenance"], "true")

    @requests_mock.Mocker()
    def test_update_alertrule_default(self, m):
        m.put(
            "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
            json=ALERTRULE,
        )

        response = self.grafana.alertingprovisioning.update_alertrule(alertrule_uid="bUUGqLiVk", alertrule=ALERTRULE)
        self.assertEqual(response["uid"], "bUUGqLiVk")

        # Verify request header.
        history = m.request_history
        headers = history[0].headers
        self.assertNotIn("X-Disable-Provenance", headers)

    @requests_mock.Mocker()
    def test_update_alertrule_disable_provenance(self, m):
        m.put(
            "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
            json=ALERTRULE,
        )

        response = self.grafana.alertingprovisioning.update_alertrule(
            alertrule_uid="bUUGqLiVk", alertrule=ALERTRULE, disable_provenance=True
        )
        self.assertEqual(response["uid"], "bUUGqLiVk")

        # Verify request header.
        history = m.request_history
        headers = history[0].headers
        self.assertIn("X-Disable-Provenance", headers)
        self.assertEqual(headers["X-Disable-Provenance"], "true")

    @requests_mock.Mocker()
    def test_delete_notification_policy_tree(self, m):
        JSON_RESPONSE = {"receiver": "grafana-default-email", "group_by": ["grafana_folder", "alertname"]}

        m.delete("http://localhost/api/v1/provisioning/policies", json=JSON_RESPONSE)
        self.grafana.alertingprovisioning.delete_notification_policy_tree()

    @requests_mock.Mocker()
    def test_delete_mute_timing(self, m):
        JSON_RESPONSE = {}
        m.delete("http://localhost/api/v1/provisioning/mute-timings/test-mute-timing", json=JSON_RESPONSE)
        self.grafana.alertingprovisioning.delete_mute_timing("test-mute-timing")

    @requests_mock.Mocker()
    def test_get_mute_timing(self, m):
        JSON_RESPONSE = {
            "name": "test-mute-timing",
            "time_intervals": [{}],
            "version": "c0764d2988e93f94",
            "provenance": "api",
        }
        m.get("http://localhost/api/v1/provisioning/mute-timings/test-mute-timing", json=JSON_RESPONSE)
        response = self.grafana.alertingprovisioning.get_mute_timing("test-mute-timing")
        self.assertEqual(response["name"], "test-mute-timing")
