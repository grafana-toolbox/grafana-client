import unittest

from grafana_client import GrafanaApi

from ..compat import requests_mock


class HealthTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_healthcheck(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json={"buildInfo": {"commit": "6f8c1d9fe4", "version": "7.5.11"}},
        )

        result = self.grafana.health.check()
        self.assertEqual(result["version"], "7.5.11")
