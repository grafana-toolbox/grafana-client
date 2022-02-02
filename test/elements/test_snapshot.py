import unittest

import requests_mock

from grafana_client import GrafanaApi


class SnapshotTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_create_new_snapshot(self, m):
        m.post(
            "http://localhost/api/snapshots",
            json={
                "deleteKey": "XXXXXXX",
                "deleteUrl": "myurl/api/snapshots.py-delete/XXXXXXX",
                "key": "YYYYYYY",
                "url": "myurl/dashboard/snapshot/YYYYYYY",
            },
        )
        snapshot = self.grafana.snapshots.create_new_snapshot(
            dashboard={
                "editable": "false",
                "hideControls": "true",
                "nav": [{"enable": "false", "type": "timepicker"}],
                "rows": [{}],
                "style": "dark",
                "tags": [],
                "templating": {"list": []},
                "time": {},
                "timezone": "browser",
                "title": "Home",
                "version": 5,
            },
            name="Test",
            key="YYYYYYY",
            delete_key="XXXXXXX",
            external=True,
            expires=3600,
        )
        self.assertEqual(snapshot["key"], "YYYYYYY")

    @requests_mock.Mocker()
    def test_create_new_snapshot_without_optional(self, m):
        m.post(
            "http://localhost/api/snapshots",
            json={
                "deleteKey": "XXXXXXX",
                "deleteUrl": "myurl/api/snapshots.py-delete/XXXXXXX",
                "key": "YYYYYYY",
                "url": "myurl/dashboard/snapshot/YYYYYYY",
            },
        )
        snapshot = self.grafana.snapshots.create_new_snapshot(
            dashboard={
                "editable": "false",
                "hideControls": "true",
                "nav": [{"enable": "false", "type": "timepicker"}],
                "rows": [{}],
                "style": "dark",
                "tags": [],
                "templating": {"list": []},
                "time": {},
                "timezone": "browser",
                "title": "Home",
                "version": 5,
            }
        )
        self.assertEqual(snapshot["key"], "YYYYYYY")

    @requests_mock.Mocker()
    def test_get_dashboard_snapshots(self, m):
        m.get(
            "http://localhost/api/dashboard/snapshots",
            json=[
                {
                    "id": 8,
                    "name": "Home",
                    "key": "YYYYYYY",
                    "orgId": 1,
                    "userId": 1,
                    "external": False,
                    "externalUrl": "",
                    "expires": "2200-13-32T25:23:23+02:00",
                    "created": "2200-13-32T28:24:23+02:00",
                    "updated": "2200-13-32T28:24:23+02:00",
                }
            ],
        )
        dashboards = self.grafana.snapshots.get_dashboard_snapshots()
        self.assertEqual(len(dashboards), 1)

    @requests_mock.Mocker()
    def test_get_snapshot_by_key(self, m):
        m.get(
            "http://localhost/api/snapshots/YYYYYYY",
            json=[
                {
                    "id": 8,
                    "name": "Home",
                    "key": "YYYYYYY",
                    "orgId": 1,
                    "userId": 1,
                    "external": False,
                    "externalUrl": "",
                    "expires": "2200-13-32T25:23:23+02:00",
                    "created": "2200-13-32T28:24:23+02:00",
                    "updated": "2200-13-32T28:24:23+02:00",
                }
            ],
        )
        dashboards = self.grafana.snapshots.get_snapshot_by_key(key="YYYYYYY")
        self.assertEqual(len(dashboards), 1)

    @requests_mock.Mocker()
    def test_delete_snapshot_by_key(self, m):
        m.delete(
            "http://localhost/api/snapshots/YYYYYYY",
            json={"message": "Snapshot deleted. It might take an hour " "before it's cleared from any CDN " "caches."},
        )
        annotation = self.grafana.snapshots.delete_snapshot_by_key(snapshot_id="YYYYYYY")
        self.assertEqual(
            annotation["message"], "Snapshot deleted. It might take an hour before it's cleared from any " "CDN caches."
        )

    @requests_mock.Mocker()
    def test_delete_snapshot_by_delete_key(self, m):
        m.get(
            "http://localhost/api/snapshots-delete/XXXXXXX",
            json={"message": "Snapshot deleted. It might take an hour " "before it's cleared from any CDN " "caches."},
        )
        annotation = self.grafana.snapshots.delete_snapshot_by_delete_key(snapshot_delete_key="XXXXXXX")
        self.assertEqual(
            annotation["message"], "Snapshot deleted. It might take an hour before it's cleared from any " "CDN caches."
        )
