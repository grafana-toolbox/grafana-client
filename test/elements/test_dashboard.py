import sys
import unittest

import pytest
from verlib2 import Version

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DashboardTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned, dashboard_basic, folder_basic):
        self.grafana = grafana_provisioned
        self.dashboard = dashboard_basic
        self.folder = folder_basic

    def test_get_dashboard_by_uid(self):
        dashboard_uid = self.dashboard["uid"]
        dashboard = self.grafana.dashboard.get_dashboard(dashboard_uid)
        self.assertEqual(dashboard["dashboard"]["uid"], dashboard_uid)

    def test_get_dashboard_by_name_grafana7(self):
        if Version(self.grafana.version) < Version("8"):
            dashboard = self.grafana.dashboard.get_dashboard_by_name("productionoverview")
            self.assertEqual(dashboard["dashboard"]["title"], "ProductionOverview")
        else:
            pytest.skip("Grafana 8 and higher does not support getting dashboards by slug")

    def test_get_dashboard_by_name_grafana8(self):
        if Version(self.grafana.version) >= Version("8"):
            with self.assertRaises(DeprecationWarning) as ex:
                self.grafana.dashboard.get_dashboard_by_name("foobar")
            self.assertEqual(
                "Grafana 8 and higher does not support getting dashboards by slug",
                str(ex.exception),
            )
        else:
            pytest.skip("Skipping test on Grafana 7 and lower")

    def test_update_dashboard_basic(self):
        """
        Verify a general dashboard update.
        """
        dashboard_uid = self.dashboard["uid"]
        dashboard = self.grafana.dashboard.update_dashboard(
            {
                "dashboard": {
                    "uid": dashboard_uid,
                    "title": "Production Overview NG",
                },
                "overwrite": True,
            }
        )
        self.assertEqual(dashboard["uid"], dashboard_uid)
        self.assertEqual(dashboard["status"], "success")
        self.assertEqual(dashboard["version"], 2)

    def test_update_dashboard_roundtrip_folder_1(self):
        """
        Verify that a dashboard update will use the "folderId"
        from the nested "meta" object.
        This is important when round-tripping dashboard payloads.
        """
        folder_id = self.folder["id"]
        folder_uid = self.folder["uid"]
        db = self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": folder_id,
                },
                "dashboard": {"title": "default"},
            }
        )
        # folderUid only exists with Grafana 11 and higher.
        if Version(self.grafana.version) >= Version("11"):
            self.assertEqual(db["folderUid"], folder_uid)

    def test_update_dashboard_roundtrip_folder_2(self):
        """
        Verify that a dashboard update will use the "folderId"
        from the toplevel dashboard payload, even if it is present
        within the nested "meta" object.
        This is important when roundtripping dashboard payloads and
        intentionally wanting to move the dashboard to a different folder.
        """
        folder_id = self.folder["id"]
        db = self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": 123,
                },
                "dashboard": {"title": "default"},
                "folderId": folder_id,
            }
        )
        db = self.grafana.dashboard.get_dashboard(db["uid"])
        self.assertEqual(db["meta"]["folderId"], folder_id)

    def test_get_home_dashboard(self):
        dashboard = self.grafana.dashboard.get_home_dashboard()
        self.assertEqual(dashboard["dashboard"]["title"], "Home")
        self.assertEqual(dashboard["meta"]["url"], "")
        if Version(self.grafana.version) < Version("9"):
            self.assertEqual(dashboard["meta"]["isHome"], True)
        if Version(self.grafana.version) >= Version("8"):
            self.assertEqual(dashboard["meta"]["canDelete"], False)

    def test_delete_dashboard(self):
        dashboard_uid = self.dashboard["uid"]
        response = self.grafana.dashboard.delete_dashboard(dashboard_uid)
        self.assertEqual(response["title"], "ProductionOverview")

    def test_get_dashboards_tags(self):
        tags = self.grafana.dashboard.get_dashboards_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0]["term"], "bazqux")

    permissions = [
        {"role": "Viewer", "permission": 1},
        {"role": "Editor", "permission": 2},
        {"teamId": 1, "permission": 1},
        {"userId": 1, "permission": 4},
    ]

    def test_dashboard_permissions_by_id(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")
        dashboard_id = self.dashboard["id"]

        response = self.grafana.dashboard.update_permissions_by_id(dashboard_id, self.permissions)
        self.assertEqual(response["message"], "Dashboard permissions updated")

        permissions = self.grafana.dashboard.get_permissions_by_id(dashboard_id)
        self.assertEqual(len(permissions), 4)

    def test_dashboard_permissions_by_uid(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Grafana 8 and earlier do not support accessing dashboards by uid for permission updates.")
        dashboard_uid = self.dashboard["uid"]

        response = self.grafana.dashboard.update_permissions_by_uid(dashboard_uid, self.permissions)
        self.assertEqual(response["message"], "Dashboard permissions updated")

        permissions = self.grafana.dashboard.get_permissions_by_uid(dashboard_uid)
        self.assertEqual(len(permissions), 4)
