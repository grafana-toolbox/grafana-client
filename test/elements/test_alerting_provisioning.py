"""
Alerting provisioning HTTP API.

Starting with v9.0, the Legacy Alerting Notification Channels API is deprecated.
It has been removed with Grafana 11.

https://grafana.com/docs/grafana/v12.0/developers/http_api/alerting_provisioning/
https://www.percona.com/blog/copying-alert-rules-from-one-percona-monitoring-and-management-server-to-another/
"""

import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client.client import GrafanaClientError, GrafanaServerError

ALERTRULE = {
    "uid": "bUUGqLiVk",
    "provenance": "api",
    "orgID": 1,
    "folderUID": "ap-folder",
    "ruleGroup": "Any",
    "title": "ApiAlerts",
    "condition": "B",
    "data": [
        {
            "refId": "A",
            "queryType": "",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": "PA58DA793C7250F1B",
            "model": {
                "expr": "max_over_time(mysql_global_status_threads_connected[5m])",
                "instant": True,
                "intervalMs": 1000,
                "maxDataPoints": 43200,
                "refId": "A",
            },
        }
    ],
    "updated": "2022-08-17T13:00:21Z",
    "noDataState": "NoData",
    "execErrState": "Alerting",
    "for": "5m",
    "labels": {"alertGroup": "any", "region": "eu-west-1"},
}

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class AlertingProvisioningTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api, reset_folders_dashboards):  # noqa: ARG002
        self.grafana = grafana_api
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Alerting provisioning supported by Grafana 9 and higher.")

        # Prune alerting rules and mute timings.
        for alertrule in self.grafana.alertingprovisioning.get_alertrules_all():
            self.grafana.alertingprovisioning.delete_alertrule(alertrule["uid"])
        for mute_timing in self.grafana.alertingprovisioning.get_mute_timings():
            self.grafana.alertingprovisioning.delete_mute_timing(mute_timing["name"])

        # Provision single alerting rule.
        self.folder = self.grafana.folder.create_folder("alert-folder", uid="ap-folder")
        self.grafana.alertingprovisioning.create_alertrule(ALERTRULE)
        self.alertrule_uid = ALERTRULE["uid"]

    def test_get_alertrules_all(self):
        response = self.grafana.alertingprovisioning.get_alertrules_all()
        self.assertEqual(response[0]["uid"], self.alertrule_uid)

    def test_get_alertrule(self):
        response = self.grafana.alertingprovisioning.get_alertrule(self.alertrule_uid)
        self.assertEqual(response["uid"], self.alertrule_uid)

    def test_delete_alertrule(self):
        self.grafana.alertingprovisioning.delete_alertrule(self.alertrule_uid)
        with self.assertRaises(GrafanaClientError) as excinfo:
            self.grafana.alertingprovisioning.get_alertrule(self.alertrule_uid)
        self.assertEqual(excinfo.exception.status_code, 404)
        self.assertRegex(excinfo.exception.message, "Client Error 404: (null|NotFound)?")

    def test_update_alertrule_standard(self):
        response = self.grafana.alertingprovisioning.update_alertrule(
            alertrule_uid=self.alertrule_uid, alertrule=ALERTRULE
        )
        self.assertEqual(response["uid"], self.alertrule_uid)

    def test_create_alertrule_disable_provenance(self):
        alertrule = ALERTRULE.copy()
        alertrule["uid"] = "ng"
        alertrule["title"] = "ng"
        response = self.grafana.alertingprovisioning.create_alertrule(alertrule, disable_provenance=True)
        self.assertEqual(response["uid"], "ng")

    def test_update_alertrule_disable_provenance(self):
        """
        cannot change provenance from 'api' to ''
        """
        with self.assertRaises(GrafanaServerError) as excinfo:
            self.grafana.alertingprovisioning.update_alertrule(
                alertrule_uid=self.alertrule_uid, alertrule=ALERTRULE, disable_provenance=True
            )
        self.assertEqual(excinfo.exception.status_code, 500)

    def test_delete_notification_policy_tree(self):
        response = self.grafana.alertingprovisioning.delete_notification_policy_tree()
        self.assertEqual(response["group_by"], ["grafana_folder", "alertname"])
        self.assertIn(response["receiver"], ["grafana-default-email", "empty"])

    def test_delete_mute_timing_success(self):
        self.grafana.alertingprovisioning.create_mute_timing(
            {
                "name": "test-mute-timing",
                "time_intervals": [{}],
                "version": "c0764d2988e93f94",
                "provenance": "api",
            }
        )
        response = self.grafana.alertingprovisioning.get_mute_timing("test-mute-timing")
        self.assertEqual(response["name"], "test-mute-timing")
        self.grafana.alertingprovisioning.delete_mute_timing("test-mute-timing")

    def test_delete_mute_timing_unknown(self):
        with self.assertRaises(GrafanaClientError) as excinfo:
            self.grafana.alertingprovisioning.get_mute_timing("unknown")
        self.assertEqual(excinfo.exception.status_code, 404)
        self.assertRegex(excinfo.exception.message, r"Client Error 404: (null|Not\s?[Ff]ound)")
