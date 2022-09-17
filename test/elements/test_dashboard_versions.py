import unittest

import requests_mock

from grafana_client import GrafanaApi


class DashboardVersionsTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    def test_api_path_success(self):
        api_path = self.grafana.dashboard_versions.api_path(dashboard_id=42)
        self.assertEqual(api_path, "/dashboards/id/42")

    def test_api_path_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.api_path()
        self.assertEqual(str(ctx.exception), "Either dashboard_id or dashboard_uid is required")

    @requests_mock.Mocker()
    def test_get_dashboard_versions_by_id(self, m):
        m.get(
            "http://localhost/api/dashboards/id/1/versions",
            json=[
                {
                    "id": 2,
                    "dashboardId": 1,
                    "parentVersion": 1,
                    "restoredFrom": 0,
                    "version": 2,
                    "created": "2017-06-08T17:24:33-04:00",
                    "createdBy": "admin",
                    "message": "Updated panel title",
                },
                {
                    "id": 1,
                    "dashboardId": 1,
                    "parentVersion": 0,
                    "restoredFrom": 0,
                    "version": 1,
                    "created": "2017-06-08T17:23:33-04:00",
                    "createdBy": "admin",
                    "message": "Initial save",
                },
            ],
        )
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_id(dashboard_id=1, limit=10, start=0)
        self.assertEqual(versions[0]["dashboardId"], 1)

    @requests_mock.Mocker()
    def test_get_dashboard_versions_by_uid(self, m):
        m.get(
            "http://localhost/api/dashboards/uid/QA7wKklGz/versions",
            json=[
                {
                    "id": 2,
                    "dashboardId": 1,
                    "uid": "QA7wKklGz",
                    "parentVersion": 1,
                    "restoredFrom": 0,
                    "version": 2,
                    "created": "2017-06-08T17:24:33-04:00",
                    "createdBy": "admin",
                    "message": "Updated panel title",
                },
                {
                    "id": 1,
                    "dashboardId": 1,
                    "uid": "QA7wKklGz",
                    "parentVersion": 0,
                    "restoredFrom": 0,
                    "version": 1,
                    "created": "2017-06-08T17:23:33-04:00",
                    "createdBy": "admin",
                    "message": "Initial save",
                },
            ],
        )
        versions = self.grafana.dashboard_versions.get_dashboard_versions_by_uid(
            dashboard_uid="QA7wKklGz", limit=10, start=0
        )
        self.assertEqual(versions[0]["uid"], "QA7wKklGz")

    @requests_mock.Mocker()
    def test_get_dashboard_version_by_id(self, m):
        m.get(
            "http://localhost/api/dashboards/id/1/versions/1",
            json={
                "id": 1,
                "dashboardId": 1,
                "parentVersion": 0,
                "restoredFrom": 0,
                "version": 1,
                "created": "2017-04-26T17:18:38-04:00",
                "message": "Initial save",
                "data": {"rows": [], "schemaVersion": 14, "timezone": "browser", "title": "test", "version": 1},
                "createdBy": "admin",
            },
        )
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_id(dashboard_id=1, version_id=1)
        self.assertEqual(dashboard["dashboardId"], 1)

    @requests_mock.Mocker()
    def test_get_dashboard_version_by_uid_success(self, m):
        m.get(
            "http://localhost/api/dashboards/uid/QA7wKklGz/versions/1",
            json={
                "id": 1,
                "dashboardId": 1,
                "uid": "QA7wKklGz",
                "parentVersion": 0,
                "restoredFrom": 0,
                "version": 1,
                "created": "2017-04-26T17:18:38-04:00",
                "message": "Initial save",
                "data": {"rows": [], "schemaVersion": 14, "timezone": "browser", "title": "test", "version": 1},
                "createdBy": "admin",
            },
        )
        dashboard = self.grafana.dashboard_versions.get_dashboard_version_by_uid(
            dashboard_uid="QA7wKklGz", version_id=1
        )
        self.assertEqual(dashboard["uid"], "QA7wKklGz")

    def test_get_dashboard_version_by_uid_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.get_dashboard_version_by_uid(dashboard_uid="QA7wKklGz")
        self.assertEqual(str(ctx.exception), "version_id is required")

    @requests_mock.Mocker()
    def test_restore_dashboard_by_id(self, m):
        m.post(
            "http://localhost/api/dashboards/id/1/restore",
            json={"slug": "my-dashboard", "status": "success", "version": 3},
        )
        result = self.grafana.dashboard_versions.restore_dashboard_by_id(dashboard_id=1, version_id=1)
        self.assertEqual(result["status"], "success")

    @requests_mock.Mocker()
    def test_restore_dashboard_by_uid_success(self, m):
        m.post(
            "http://localhost/api/dashboards/uid/QA7wKklGz/restore",
            json={
                "id": 70,
                "slug": "my-dashboard",
                "status": "success",
                "uid": "QA7wKklGz",
                "url": "/d/QA7wKklGz/my-dashboard",
                "version": 3,
            },
        )
        result = self.grafana.dashboard_versions.restore_dashboard_by_uid(dashboard_uid="QA7wKklGz", version_id=1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["uid"], "QA7wKklGz")

    def test_restore_dashboard_by_uid_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.restore_dashboard_by_uid(dashboard_uid="QA7wKklGz")
        self.assertEqual(str(ctx.exception), "version_id is required")

    @requests_mock.Mocker()
    def test_calculate_diff_success(self, m):
        m.post(
            "http://localhost/api/dashboards/calculate-diff",
            headers={"Content-Type": "text/html; charset=UTF-8"},
            text="""
<p id="l1" class="diff-line diff-json-same">
  <!-- Diff omitted -->
</p>
""",
        )
        result = self.grafana.dashboard_versions.calculate_diff(
            base_dashboard_id=1, base_version_id=1, new_dashboard_id=1, new_version_id=2
        )
        self.assertIn("diff-json", result)

    def test_calculate_diff_failure(self):
        with self.assertRaises(LookupError) as ctx:
            self.grafana.dashboard_versions.calculate_diff(
                base_dashboard_id=1, base_version_id=1, new_dashboard_id=1, new_version_id=2, diff_type="foobar"
            )
        self.assertEqual(str(ctx.exception), "diff_type must be either 'json' or 'basic'")
