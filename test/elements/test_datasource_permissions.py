"""
Data Source Permissions is only available in Grafana Enterprise and Grafana Cloud.

https://grafana.com/docs/grafana/latest/administration/data-source-management/
https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/datasource_permissions/
"""

import os
import sys
import unittest

import pytest

from test.elements.test_datasource_fixtures import PROMETHEUS_DATASOURCE

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
@unittest.skipIf(
    not os.environ.get("GRAFANA_ENTERPRISE"),
    "Datasource permissions only available in Grafana Enterprise and Grafana Cloud",
)
class DatasourceTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned, dashboard_basic, folder_basic):
        self.grafana = grafana_provisioned
        self.dashboard = dashboard_basic
        self.folder = folder_basic
        self.datasource = self.grafana.datasource.create_datasource(PROMETHEUS_DATASOURCE)
        self.datasource_id = self.datasource["datasource"]["id"]
        self.datasource_uid = self.datasource["datasource"]["uid"]

    def test_enable_datasource_permissions(self):
        result = self.grafana.datasource.enable_datasource_permissions(self.datasource_id)
        self.assertEqual(result, {"message": "Datasource permissions enabled"})

    def test_disable_datasource_permissions(self):
        result = self.grafana.datasource.disable_datasource_permissions(self.datasource_id)
        self.assertEqual(result, {"message": "Datasource permissions disabled"})

    def test_get_datasource_permissions(self):
        result = self.grafana.datasource.get_datasource_permissions(self.datasource_id)
        self.assertEqual(result["datasourceId"], self.datasource_id)

    def test_add_datasource_permissions(self):
        result = self.grafana.datasource.add_datasource_permissions(self.datasource_id, {"userId": 1, "permission": 1})
        self.assertEqual(result, {"message": "Datasource permission added"})

    def test_remove_datasource_permissions(self):
        result = self.grafana.datasource.remove_datasource_permissions(self.datasource_id, 1)
        self.assertEqual(result, {"message": "Datasource permission removed"})
