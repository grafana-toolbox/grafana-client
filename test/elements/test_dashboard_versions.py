import sys
import unittest

import pytest
from verlib2 import Version

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DashboardVersionsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api, dashboard_uid: str, dashboard_id: int):
        self.grafana = grafana_api
        self.dashboard_id = dashboard_id
        self.dashboard_uid = dashboard_uid

    def test_api_path_success(self):
        api_path = self.grafana.dashboard_versions.api_path(dashboard_id=42)
        self.assertEqual(api_path, "/dashboards/id/42")

    def test_api_path_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.api_path()
        self.assertEqual(str(ctx.exception), "Either dashboard_id or dashboard_uid is required")

    def test_get_dashboard_versions_by_id(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_id(
            dashboard_id=self.dashboard_id, limit=10, start=0
        )
        if Version(self.grafana.version) >= Version("11"):
            versions = versions["versions"]
        self.assertEqual(versions[0]["dashboardId"], self.dashboard_id)

    def test_get_dashboard_versions_by_uid(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Grafana 8 and earlier do not support accessing dashboard versions by uid.")
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_uid(
            dashboard_uid=self.dashboard_uid, limit=10, start=0
        )
        if Version(self.grafana.version) >= Version("11"):
            versions = versions["versions"]
        self.assertEqual(versions[0]["uid"], self.dashboard_uid)

    def test_get_dashboard_version_by_id(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_id(
            dashboard_id=self.dashboard_id, version_id=1
        )
        self.assertEqual(dashboard["dashboardId"], self.dashboard_id)

    def test_get_dashboard_version_by_uid_success(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Grafana 8 and earlier do not support accessing dashboard versions by uid.")
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_uid(
            dashboard_uid=self.dashboard_uid, version_id=1
        )
        self.assertEqual(dashboard["uid"], self.dashboard_uid)

    def test_get_dashboard_version_by_uid_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.get_dashboard_version_by_uid(dashboard_uid=self.dashboard_uid)
        self.assertEqual(str(ctx.exception), "version_id is required")

    def test_restore_dashboard_by_id_success(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")
        result = self.grafana.dashboard_versions.restore_dashboard_by_id(dashboard_id=self.dashboard_id, version_id=1)
        self.assertEqual(result["status"], "success")

    def test_restore_dashboard_by_uid_success(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Grafana 8 and earlier do not support accessing dashboards by uid for restoring dashboards.")
        self.update_dashboard()
        result = self.grafana.dashboard_versions.restore_dashboard_by_uid(
            dashboard_uid=self.dashboard_uid, version_id=1
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["uid"], self.dashboard_uid)

    def test_restore_dashboard_by_uid_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.restore_dashboard_by_uid(dashboard_uid=self.dashboard_uid)
        self.assertEqual(str(ctx.exception), "version_id is required")

    def test_calculate_diff_success(self):
        if Version(self.grafana.version) >= Version("9"):
            pytest.skip(
                "Grafana 8 and higher do dashboard diffing entirely in the frontend, "
                "Grafana 9 deprecated corresponding backend support."
            )
        self.update_dashboard()
        result = self.grafana.dashboard_versions.calculate_diff(
            base_dashboard_id=self.dashboard_id,
            base_version_id=1,
            new_dashboard_id=self.dashboard_id,
            new_version_id=2,
        )
        self.assertIn("diff-json", result)

    def test_calculate_diff_failure(self):
        if Version(self.grafana.version) >= Version("9"):
            pytest.skip(
                "Grafana 8 and higher do dashboard diffing entirely in the frontend, "
                "Grafana 9 deprecated corresponding backend support."
            )
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.calculate_diff(
                base_dashboard_id=self.dashboard_id,
                base_version_id=1,
                new_dashboard_id=self.dashboard_id,
                new_version_id=2,
                diff_type="foobar",
            )
        self.assertEqual(str(ctx.exception), "diff_type must be either 'json' or 'basic'")

    def update_dashboard(self):
        """
        Helper to update the default dashboard to receive another version.
        """
        self.grafana.dashboard.update_dashboard(
            {
                "dashboard": {
                    "uid": self.dashboard_uid,
                    "title": "Production Overview NG",
                },
                "overwrite": True,
            }
        )
