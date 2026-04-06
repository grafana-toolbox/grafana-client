import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client.client import GrafanaBadInputError, GrafanaClientError
from grafana_client.model import PersonalPreferences

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DashboardTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api,
        dashboard_folder_permissions,
        dashboard_id: int,
        dashboard_uid: str,
        folder_id: str,
        folder_uid: str,
    ):
        self.grafana = grafana_api
        self.dashboard_id = dashboard_id
        self.dashboard_uid = dashboard_uid
        self.folder_id = folder_id
        self.folder_uid = folder_uid
        self.permissions = dashboard_folder_permissions

    def test_get_dashboard_by_uid(self):
        dashboard = self.grafana.dashboard.get_dashboard(self.dashboard_uid)
        self.assertEqual(dashboard["dashboard"]["uid"], self.dashboard_uid)

    def test_get_dashboard_by_name_grafana7(self):
        if Version(self.grafana.version) < Version("8"):
            dashboard = self.grafana.dashboard.get_dashboard_by_name("productionoverview")
            self.assertEqual(dashboard["dashboard"]["title"], "ProductionOverview")
        else:
            pytest.skip("Grafana 8 and higher does not support getting dashboards by slug")

    def test_get_dashboard_by_name(self):
        def probe():
            return self.grafana.dashboard.get_dashboard_by_name("productionoverview")

        if Version(self.grafana.version) >= Version("8"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("Not found", context.exception.message)
        else:
            dashboard = probe()
            self.assertEqual(self.dashboard_uid, dashboard["dashboard"]["uid"])

    def test_update_dashboard_standard(self):
        """Verify a general dashboard update."""
        dashboard = self.grafana.dashboard.update_dashboard(
            {
                "dashboard": {
                    "uid": self.dashboard_uid,
                    "title": "Production Overview NG",
                },
                "overwrite": True,
            }
        )
        self.assertEqual(dashboard["uid"], self.dashboard_uid)
        self.assertEqual(dashboard["status"], "success")
        self.assertEqual(dashboard["version"], 2)

    def test_update_dashboard_roundtrip_folder_1(self):
        """
        Verify that a dashboard update will use the "folderId"
        from the nested "meta" object.
        This is important when round-tripping dashboard payloads.
        """
        db = self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": self.folder_id,
                },
                "dashboard": {"title": "default"},
            }
        )
        # folderUid only exists with Grafana 11 and higher.
        if Version(self.grafana.version) >= Version("11"):
            self.assertEqual(db["folderUid"], self.folder_uid)

    def test_update_dashboard_roundtrip_folder_2(self):
        """
        Verify that a dashboard update will use the "folderId"
        from the toplevel dashboard payload, even if it is present
        within the nested "meta" object.
        This is important when roundtripping dashboard payloads and
        intentionally wanting to move the dashboard to a different folder.
        """
        db = self.grafana.dashboard.update_dashboard(
            {
                "meta": {
                    "folderId": 123,
                },
                "dashboard": {"title": "default"},
                "folderId": self.folder_id,
            }
        )
        db = self.grafana.dashboard.get_dashboard(db["uid"])
        self.assertEqual(db["meta"]["folderId"], self.folder_id)

    def test_get_home_dashboard(self):
        self.grafana.user.update_preferences(PersonalPreferences(homeDashboardId=self.dashboard_id))
        dashboard = self.grafana.dashboard.get_home_dashboard()
        assert dashboard == {"redirectUri": "/d/cIBgcSjkk/productionoverview"}
        # TODO: The original response looks like this. However, as soon as the personal preferences
        #       will be updated, we haven't found a way to deterministically restore the original content
        #       per Grafana API. This is why the test case now calls `update_preferences` and validates
        #       the `redirectUri` response payload to provide a stable outcome.
        #       Any suggestions to improve are welcome.
        """
        self.assertEqual(dashboard["dashboard"]["title"], "Home")
        self.assertEqual(dashboard["meta"]["url"], "")
        if Version(self.grafana.version) < Version("9"):
            self.assertEqual(dashboard["meta"]["isHome"], True)
        if Version(self.grafana.version) >= Version("8"):
            self.assertEqual(dashboard["meta"]["canDelete"], False)
        """

    def test_delete_dashboard(self):
        response = self.grafana.dashboard.delete_dashboard(self.dashboard_uid)
        self.assertEqual(response["title"], "ProductionOverview")

    def test_get_dashboards_tags(self):
        tags = self.grafana.dashboard.get_dashboards_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0]["term"], "bazqux")

    def test_dashboard_permissions_by_id(self):
        grafana8 = Version("8") <= Version(self.grafana.version) < Version("9")
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing dashboards by id, use uids instead.")

        if grafana8:
            with self.assertRaises(GrafanaBadInputError) as context:
                self.grafana.dashboard.update_permissions_by_id(self.dashboard_id, self.permissions)
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("you can only override a permission to be higher", context.exception.message)
            return

        response = self.grafana.dashboard.update_permissions_by_id(self.dashboard_id, self.permissions)
        self.assertEqual(response["message"], "Dashboard permissions updated")

        permissions = self.grafana.dashboard.get_permissions_by_id(self.dashboard_id)
        self.assertEqual(len(permissions), 4)

    def test_dashboard_permissions_by_uid(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Grafana 8 and earlier do not support accessing dashboards by uid for permission updates.")

        response = self.grafana.dashboard.update_permissions_by_uid(self.dashboard_uid, self.permissions)
        self.assertEqual(response["message"], "Dashboard permissions updated")

        permissions = self.grafana.dashboard.get_permissions_by_uid(self.dashboard_uid)
        self.assertEqual(len(permissions), 4)
