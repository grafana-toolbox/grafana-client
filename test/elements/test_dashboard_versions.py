import sys
import unittest

import pytest
from verlib2 import Version

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DashboardVersionsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned, dashboard_basic):
        self.grafana = grafana_provisioned
        self.dashboard = dashboard_basic

    def test_api_path_success(self):
        api_path = self.grafana.dashboard_versions.api_path(dashboard_id=42)
        self.assertEqual(api_path, "/dashboards/id/42")

    def test_api_path_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.api_path()
        self.assertEqual(str(ctx.exception), "Either dashboard_id or dashboard_uid is required")

    def test_get_dashboard_versions_by_id(self):
        dashboard_id = self.dashboard["id"]
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_id(
            dashboard_id=dashboard_id, limit=10, start=0
        )
        self.assertEqual(versions["versions"][0]["dashboardId"], dashboard_id)

    def test_get_dashboard_versions_by_uid(self):
        dashboard_uid = self.dashboard["uid"]
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_uid(
            dashboard_uid=dashboard_uid, limit=10, start=0
        )
        self.assertEqual(versions["versions"][0]["uid"], dashboard_uid)

    def test_get_dashboard_version_by_id(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")
        dashboard_id = self.dashboard["id"]
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_id(dashboard_id=dashboard_id, version_id=1)
        self.assertEqual(dashboard["dashboardId"], dashboard_id)

    def test_get_dashboard_version_by_uid_success(self):
        dashboard_uid = self.dashboard["uid"]
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_uid(
            dashboard_uid=dashboard_uid, version_id=1
        )
        self.assertEqual(dashboard["uid"], dashboard_uid)

    def test_get_dashboard_version_by_uid_failure(self):
        dashboard_uid = self.dashboard["uid"]
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.get_dashboard_version_by_uid(dashboard_uid=dashboard_uid)
        self.assertEqual(str(ctx.exception), "version_id is required")

    def test_restore_dashboard_by_id_success(self):
        dashboard_id = self.dashboard["id"]
        result = self.grafana.dashboard_versions.restore_dashboard_by_id(dashboard_id=dashboard_id, version_id=1)
        self.assertEqual(result["status"], "success")

    def test_restore_dashboard_by_uid_success(self):
        dashboard_uid = self.dashboard["uid"]
        result = self.grafana.dashboard_versions.restore_dashboard_by_uid(dashboard_uid=dashboard_uid, version_id=1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["uid"], dashboard_uid)

    def test_restore_dashboard_by_uid_failure(self):
        dashboard_uid = self.dashboard["uid"]
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.restore_dashboard_by_uid(dashboard_uid=dashboard_uid)
        self.assertEqual(str(ctx.exception), "version_id is required")

    def test_calculate_diff_success(self):
        if Version(self.grafana.version) >= Version("10"):
            pytest.skip("Grafana 8 and higher do dashboard diffing entirely in the frontend.")
        dashboard_uid = self.dashboard["uid"]
        self.grafana.dashboard.update_dashboard(
            {
                "dashboard": {
                    "uid": dashboard_uid,
                    "title": "Production Overview NG",
                    "tags": ["nothing", "special"],
                    "timezone": "browser",
                },
                "overwrite": True,
            }
        )
        result = self.grafana.dashboard_versions.calculate_diff(
            base_dashboard_id=1, base_version_id=1, new_dashboard_id=1, new_version_id=2
        )
        self.assertIn("diff-json", result)

    def test_calculate_diff_failure(self):
        if Version(self.grafana.version) >= Version("10"):
            pytest.skip("Grafana 8 and higher do dashboard diffing entirely in the frontend.")
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.calculate_diff(
                base_dashboard_id=1, base_version_id=1, new_dashboard_id=1, new_version_id=2, diff_type="foobar"
            )
        self.assertEqual(str(ctx.exception), "diff_type must be either 'json' or 'basic'")
