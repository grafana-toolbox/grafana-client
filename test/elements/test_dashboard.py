import unittest

import requests_mock

from grafana_client import GrafanaApi


class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_dashboard(self, m):
        m.get(
            "http://localhost/api/dashboards/uid/cIBgcSjkk",
            json={
                "dashboard": {
                    "id": 1,
                    "uid": "cIBgcSjkk",
                    "title": "Production Overview",
                    "tags": ["templated"],
                    "timezone": "browser",
                    "schemaVersion": 16,
                    "version": 0,
                },
                "meta": {
                    "isStarred": "false",
                    "url": "/d/cIBgcSjkk/production-overview",
                    "slug": "production-overview",
                },
            },
        )
        dashboard = self.grafana.dashboard.get_dashboard("cIBgcSjkk")
        self.assertEqual(dashboard["dashboard"]["uid"], "cIBgcSjkk")

    @requests_mock.Mocker()
    def test_get_dashboard_by_name(self, m):
        m.get(
            "http://localhost/api/dashboards/db/Production Overview",
            json={
                "dashboard": {
                    "id": 1,
                    "uid": "cIBgcSjkk",
                    "title": "Production Overview",
                    "tags": ["templated"],
                    "timezone": "browser",
                    "schemaVersion": 16,
                    "version": 0,
                },
                "meta": {
                    "isStarred": "false",
                    "url": "/d/cIBgcSjkk/production-overview",
                    "slug": "production-overview",
                },
            },
        )
        dashboard = self.grafana.dashboard.get_dashboard_by_name("Production Overview")
        self.assertEqual(dashboard["dashboard"]["title"], "Production Overview")

    @requests_mock.Mocker()
    def test_update_dashboard(self, m):
        """
        Verify a general dashboard update.
        """
        m.post(
            "http://localhost/api/dashboards/db",
            json={
                "id": 1,
                "uid": "cIBgcSjkk",
                "url": "/d/cIBgcSjkk/production-overview",
                "status": "success",
                "version": 1,
                "slug": "production-overview",
            },
        )
        dashboard = self.grafana.dashboard.update_dashboard(
            {
                "dashboard": {
                    "id": 1,
                    "uid": "cIBgcSjkk",
                    "title": "Production Overview",
                    "tags": ["templated"],
                    "timezone": "browser",
                    "schemaVersion": 16,
                    "version": 0,
                },
                "folderId": 0,
                "overwrite": "false",
            }
        )

        self.assertEqual(dashboard["uid"], "cIBgcSjkk")
        self.assertEqual(dashboard["status"], "success")

    @requests_mock.Mocker()
    def test_update_dashboard_roundtrip_folder_1(self, m):
        """
        Verify that a dashboard update will use the "folderId"
        from the nested "meta" object.
        This is important when roundtripping dashboard payloads.
        """
        m.post("http://localhost/api/dashboards/db", json={})
        self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": 123,
                },
                "dashboard": {},
            }
        )

        self.assertEqual(m.last_request.json()["folderId"], 123)

    @requests_mock.Mocker()
    def test_update_dashboard_roundtrip_folder_2(self, m):
        """
        Verify that a dashboard update will use the "folderId"
        from the toplevel dashboard payload, even if it is present
        within the nested "meta" object.
        This is important when roundtripping dashboard payloads and
        intentionally wanting to move the dashboard to a different folder.
        """
        m.post("http://localhost/api/dashboards/db", json={})
        self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": 123,
                },
                "dashboard": {},
                "folderId": 456,
            }
        )

        self.assertEqual(m.last_request.json()["folderId"], 456)

    @requests_mock.Mocker()
    def test_get_home_dashboard(self, m):
        m.get(
            "http://localhost/api/dashboards/home",
            json={
                "dashboard": {
                    "editable": "false",
                    "hideControls": "true",
                    "nav": [{"enable": "false", "type": "timepicker"}],
                    "style": "dark",
                    "tags": [],
                    "templating": {"list": []},
                    "time": {},
                    "timezone": "browser",
                    "title": "Home",
                    "version": 5,
                },
                "meta": {
                    "isHome": "true",
                    "canSave": "false",
                    "canEdit": "false",
                    "canStar": "false",
                    "url": "",
                    "expires": "0001-01-01T00:00:00Z",
                    "created": "0001-01-01T00:00:00Z",
                },
            },
        )
        dashboard = self.grafana.dashboard.get_home_dashboard()
        self.assertEqual(dashboard["meta"]["isHome"], "true")

    @requests_mock.Mocker()
    def test_delete_dashboard(self, m):
        m.delete("http://localhost/api/dashboards/uid/cIBgcSjkk", json={"title": "Production Overview"})
        response = self.grafana.dashboard.delete_dashboard("cIBgcSjkk")
        self.assertEqual(response["title"], "Production Overview")

    @requests_mock.Mocker()
    def test_get_dashboards_tags(self, m):
        m.get("http://localhost/api/dashboards/tags", json=[{"term": "tag1", "count": 1}, {"term": "tag2", "count": 4}])
        tags = self.grafana.dashboard.get_dashboards_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0]["term"], "tag1")

    @requests_mock.Mocker()
    def test_get_dashboard_permissions(self, m):
        m.get(
            "http://localhost/api/dashboards/id/1/permissions",
            json=[
                {
                    "id": 1,
                    "dashboardId": 1,
                    "created": "2017-06-20T02:00:00+02:00",
                    "updated": "2017-06-20T02:00:00+02:00",
                    "userId": 0,
                    "userLogin": "",
                    "userEmail": "",
                    "teamId": 0,
                    "team": "",
                    "role": "Viewer",
                    "permission": 1,
                    "permissionName": "View",
                    "uid": "",
                    "title": "",
                    "slug": "",
                    "isFolder": "false",
                    "url": "",
                },
                {
                    "id": 2,
                    "dashboardId": 1,
                    "created": "2017-06-20T02:00:00+02:00",
                    "updated": "2017-06-20T02:00:00+02:00",
                    "userId": 0,
                    "userLogin": "",
                    "userEmail": "",
                    "teamId": 0,
                    "team": "",
                    "role": "Editor",
                    "permission": 2,
                    "permissionName": "Edit",
                    "uid": "",
                    "title": "",
                    "slug": "",
                    "isFolder": "false",
                    "url": "",
                },
            ],
        )
        permissions = self.grafana.dashboard.get_dashboard_permissions(1)
        self.assertEqual(len(permissions), 2)
        self.assertEqual(permissions[0]["dashboardId"], 1)

    @requests_mock.Mocker()
    def test_update_dashboard_permissions(self, m):
        m.post("http://localhost/api/dashboards/id/1/permissions", json={"message": "Dashboard permissions updated"})
        permissions = self.grafana.dashboard.update_dashboard_permissions(
            1,
            {
                "items": [
                    {"role": "Viewer", "permission": 1},
                    {"role": "Editor", "permission": 2},
                    {"teamId": 1, "permission": 1},
                    {"userId": 11, "permission": 4},
                ]
            },
        )
        self.assertEqual(permissions["message"], "Dashboard permissions updated")
