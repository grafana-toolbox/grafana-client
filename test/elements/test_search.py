import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaServerError

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class SearchTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self, grafana_provisioned: GrafanaApi, dashboard_basic, folder_basic, dashboard_uid: str, folder_uid: str
    ):
        self.grafana = grafana_provisioned
        self.dashboard_basic = dashboard_basic
        self.folder_basic = folder_basic
        self.dashboard_uid = dashboard_uid
        self.folder_uid = folder_uid

        self.dashboard_id = self.dashboard_basic["id"]
        self.folder_id = self.folder_basic["id"]

    def test_search_dashboards_no_input(self):
        result = self.grafana.search.search_dashboards()
        self.assertEqual(2, len(result), "Wrong number of dashboards")

    def test_search_dashboards_no_results(self):
        result = self.grafana.search.search_dashboards(
            query="Hotzenplotz",
        )
        self.assertEqual(0, len(result), "Wrong number of dashboards")

    def test_search_dashboards_by_query_title(self):
        result = self.grafana.search.search_dashboards(
            query="production",
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_dashboards_by_query_tags(self):
        if Version(self.grafana.version) < Version("12"):
            pytest.skip("Dashboard tags are only indexed on Grafana 12 and higher.")
        result = self.grafana.search.search_dashboards(
            query="foobar",
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_dashboards_by_id(self):
        result = self.grafana.search.search_dashboards(
            dashboard_ids=self.dashboard_id,
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_dashboards_by_uid(self):
        result = self.grafana.search.search_dashboards(
            dashboard_uids=self.dashboard_uid,
        )
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(1, len(result), "Wrong number of dashboards")
            self.assertEqual(self.dashboard_uid, result[0]["uid"])
        else:
            self.assertEqual(2, len(result), "Wrong number of dashboards")

    def test_search_dashboards_by_tag(self):
        result = self.grafana.search.search_dashboards(
            tag="bazqux",
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_folder_by_id(self):
        result = self.grafana.search.search_dashboards(
            folder_ids=self.folder_id,
            type_="dash-folder",
        )
        if Version(self.grafana.version) >= Version("12"):
            self.assertEqual(1, len(result), "Wrong number of folders")
            self.assertEqual(self.folder_uid, result[0]["uid"])
        else:
            self.assertEqual(0, len(result), "Wrong number of folders")

    def test_search_dashboards_by_folder_uid(self):
        result = self.grafana.search.search_dashboards(
            folder_uids=self.folder_uid,
            type_="dash-db",
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_dashboards_by_type_dash(self):
        result = self.grafana.search.search_dashboards(
            type_="dash-db",
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
        self.assertEqual(self.dashboard_uid, result[0]["uid"])

    def test_search_dashboards_by_type_folder(self):
        result = self.grafana.search.search_dashboards(
            type_="dash-folder",
        )
        self.assertEqual(1, len(result), "Wrong number of folders")
        self.assertEqual(self.folder_uid, result[0]["uid"])

    def test_search_dashboards_by_type_unknown(self):
        def probe():
            return self.grafana.search.search_dashboards(
                type_="unknown",
            )

        if Version(self.grafana.version) >= Version("12"):
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("Search failed", context.exception.message)
        else:
            result = probe()
            self.assertEqual(2, len(result), "Wrong number of dashboards/folders")

    def test_search_dashboards_by_starred_false(self):
        result = self.grafana.search.search_dashboards(
            starred=False,
        )
        self.assertEqual(2, len(result), "Wrong number of dashboards")

    def test_search_dashboards_by_starred_true(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Unable to star dashboard by uid with Grafana 8 and earlier.")
        # TODO: It looks like starring a dashboard hasn't made it into an API wrapper yet.
        self.grafana.client.POST(f"/user/stars/dashboard/uid/{self.dashboard_uid}")
        result = self.grafana.search.search_dashboards(
            starred=True,
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")

    def test_search_dashboards_with_limit_success(self):
        result = self.grafana.search.search_dashboards(
            query="production",
            limit=1,
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")

    def test_search_dashboards_with_page_success(self):
        result = self.grafana.search.search_dashboards(
            query="production",
            page=2,
        )
        self.assertEqual(0, len(result), "Wrong number of dashboards")

    def test_search_dashboards_with_limit_zero(self):
        result = self.grafana.search.search_dashboards(
            query="production",
            limit=0,
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")

    def test_search_dashboards_with_page_zero(self):
        result = self.grafana.search.search_dashboards(
            query="production",
            page=0,
        )
        self.assertEqual(1, len(result), "Wrong number of dashboards")
