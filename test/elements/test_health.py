import unittest

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
    GrafanaUnauthorizedError,
)


class HealthTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_search_dashboards(self, m):
        m.get(
            "http://localhost/api/health",
<<<<<<< HEAD
            json=[
                {
                    "commit": "6f8c1d9fe4",
                    "database": "ok",
                    "version": "7.5.11"
                }
            ],
        )

        result = self.grafana.health.check()
        self.assertEqual(result[0]["database"], 'ok')
=======
            json=[{"commit": "6f8c1d9fe4", "database": "ok", "version": "7.5.11"}],
        )

        result = self.grafana.health.check()
        self.assertEqual(result[0]["database"], "ok")
>>>>>>> 0ffbd789b43184eb9fed8ca6486565b90b603aa1
        self.assertEqual(len(result), 1)
