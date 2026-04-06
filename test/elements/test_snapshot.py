import sys
import typing as t
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError, GrafanaServerError

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class SnapshotTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi, dashboard_uid: str):
        self.grafana = grafana_api
        self.dashboard_uid = dashboard_uid

        # Prune snapshots.
        for snap in self.grafana.snapshots.get_dashboard_snapshots():
            self.grafana.snapshots.delete_snapshot_by_key(snap["key"])

        # Create single snapshot.
        self.snapshot = self.grafana.snapshots.create_new_snapshot(
            dashboard={
                "uid": self.dashboard_uid,
                "editable": False,
                "nav": [{"enable": False, "type": "timepicker"}],
                "rows": [{}],
                "style": "dark",
                "tags": [],
                "templating": {"list": []},
                "time": {},
                "timezone": "browser",
                "title": "test-snapshot",
                "version": 3,
            },
            name="test-snapshot",
            key="YYYYYYY",
            delete_key="XXXXXXX",
            external=False,
            expires=3600,
        )

    def test_create_new_snapshot_standard(self):
        # Just validate that the snapshot was created.
        self.assertEqual("YYYYYYY", self.snapshot["key"])

    def test_get_all_snapshots(self):
        dashboards = self.grafana.snapshots.get_dashboard_snapshots()
        self.assertEqual(1, len(dashboards))

    def test_get_snapshot_by_key_success(self):
        snapshot = self.grafana.snapshots.get_snapshot_by_key(key="YYYYYYY")
        self.assertIn("dashboard", snapshot)
        self.assertIn("meta", snapshot)

    def test_get_snapshot_by_key_unknown(self):
        def probe():
            self.grafana.snapshots.get_snapshot_by_key(key="unknown")

        self.wrap_notfound(probe)

    def test_delete_snapshot_by_key_success(self):
        response = self.grafana.snapshots.delete_snapshot_by_key(snapshot_id="YYYYYYY")
        self.assertEqual(
            "Snapshot deleted. It might take an hour before it's cleared from any CDN caches.",
            response["message"],
        )

    def test_delete_snapshot_by_key_unknown(self):
        def probe():
            self.grafana.snapshots.delete_snapshot_by_key(snapshot_id="unknown")

        self.wrap_notfound(probe)

    def test_delete_snapshot_by_delete_key_success(self):
        response = self.grafana.snapshots.delete_snapshot_by_delete_key(snapshot_delete_key="XXXXXXX")
        self.assertEqual(
            "Snapshot deleted. It might take an hour before it's cleared from any CDN caches.",
            response["message"],
        )

    def test_delete_snapshot_by_delete_key_unknown(self):
        def probe():
            self.grafana.snapshots.delete_snapshot_by_delete_key(snapshot_delete_key="unknown")

        self.wrap_notfound(probe)

    def wrap_notfound(self, probe: t.Callable):
        grafana_version = Version(self.grafana.version)
        if grafana_version >= Version("9"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("Snapshot not found", context.exception.message)
        elif grafana_version >= Version("8"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("Failed to find dashboard snapshot", context.exception.message)
        else:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code)
            self.assertIn("Failed to get dashboard snapshot", context.exception.message)
