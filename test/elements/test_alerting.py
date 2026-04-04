import sys
import unittest

import pytest
from verlib2 import Version

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


pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class AlertingTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned):
        self.grafana = grafana_provisioned
        if Version(self.grafana.version) < Version("8"):
            pytest.skip("Alert rules: Not supported on Grafana 7 and earlier.")

        # FIXME: Why doesn't this work on Grafana 11 and higher?
        if Version(self.grafana.version) >= Version("11"):
            pytest.skip("Alert rules: Access denied starting with Grafana 11.")

        self.folder = self.grafana.folder.create_folder("alert-folder")

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
        self.grafana.alerting.create_alertrule("alert-folder", alertrule=ALERTRULE)

    def test_update_alertrule(self):
        response = self.grafana.alerting.update_alertrule("alert-folder", alertrule=ALERTRULE)
        self.assertEqual(response["message"], "no changes detected in the rule group")
