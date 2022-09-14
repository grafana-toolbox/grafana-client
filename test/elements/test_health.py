import unittest

import requests_mock

from grafana_client import GrafanaApi


class HealthTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_search_dashboards(self, m):
        m.get(
            "http://localhost/api/health",
            json=[{"commit": "6f8c1d9fe4", "database": "ok", "version": "7.5.11"}],
        )

        result = self.grafana.health.check()
        self.assertEqual(result[0]["database"], "ok")
        self.assertEqual(len(result), 1)
