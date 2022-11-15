import unittest

import requests_mock

from grafana_client import GrafanaApi

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


class AlertingTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_alertrule(self, m):
        m.get("http://localhost/api/ruler/grafana/api/v1/rules/alert-folder/alert-rule-test", json=ALERTRULE)
        response = self.grafana.alerting.get_alertrule("alert-folder", "alert-rule-test")
        self.assertEqual(response["uid"], "bUUGqLiVk")
        self.assertEqual(response["name"], "alert-rule-test")

    @requests_mock.Mocker()
    def test_delete_alertrule(self, m):
        m.delete(
            "http://localhost/api/ruler/grafana/api/v1/rules/alert-folder/alert-rule-test", json={"uid": "bUUGqLiVk"}
        )
        response = self.grafana.alerting.delete_alertrule("alert-folder", "alert-rule-test")
        self.assertEqual(response["uid"], "bUUGqLiVk")

    @requests_mock.Mocker()
    def test_create_alertrule(self, m):
        m.post(
            "http://localhost/api/ruler/grafana/api/v1/rules/alert-folder",
            json=ALERTRULE,
        )

        response = self.grafana.alerting.create_alertrule("alert-folder", ALERTRULE)
        self.assertEqual(response["uid"], "bUUGqLiVk")
        self.assertEqual(response["name"], "alert-rule-test")

    @requests_mock.Mocker()
    def test_update_alertrule(self, m):
        m.post(
            "http://localhost/api/ruler/grafana/api/v1/rules/alert-folder",
            json=ALERTRULE,
        )

        response = self.grafana.alerting.update_alertrule("alert-folder", alertrule=ALERTRULE)
        self.assertEqual(response["uid"], "bUUGqLiVk")
