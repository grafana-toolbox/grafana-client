import unittest

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError

from ..compat import requests_mock


class AnnotationsTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_search_dashboards(self, m):
        m.get(
            "http://localhost/api/search?folderIds=11&query=str_e&starred=false&tag=test_tag"
            "&type=dash-folder&dashboardIds=163&limit=10",
            json=[
                {
                    "id": 163,
                    "uid": "000000163",
                    "title": "Folder",
                    "url": "/dashboards/f/000000163/folder",
                    "type": "dash-folder",
                    "tags": [],
                    "isStarred": "false",
                    "uri": "db/folder",
                }
            ],
        )

        result = self.grafana.search.search_dashboards(
            query="str_e",
            folder_ids=11,
            starred="false",
            tag="test_tag",
            type_="dash-folder",
            dashboard_ids=163,
            limit=10,
        )
        self.assertEqual(result[0]["id"], 163)
        self.assertEqual(len(result), 1)

    @requests_mock.Mocker()
    def test_search_dashboards_with_out_filter(self, m):
        m.get(
            "http://localhost/api/search",
            json={"message": "Not found"},
            status_code=400,
        )

        with self.assertRaises(GrafanaBadInputError):
            self.grafana.search.search_dashboards()

    @requests_mock.Mocker()
    def test_search_dashboards_with_page(self, m):
        m.get(
            "http://localhost/api/search?page=1",
            json=[
                {
                    "id": 2307,
                    "uid": "LfQAz3t4z1DSA",
                    "title": "ERRORS",
                    "uri": "db/errors",
                    "url": "/d/LfQAz3t4z1DSA/errors",
                    "slug": "",
                    "type": "dash-db",
                    "tags": [],
                    "isStarred": False,
                    "sortMeta": 0,
                }
            ],
        )

        result = self.grafana.search.search_dashboards(
            page=1,
        )
        self.assertEqual(result[0]["id"], 2307)
        self.assertEqual(len(result), 1)
