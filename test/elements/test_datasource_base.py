import sys
import time
import unittest
from unittest.mock import Mock, patch

import pytest
from verlib2 import Version

from grafana_client.client import (
    GrafanaClientError,
    GrafanaServerError,
)
from grafana_client.model import DatasourceIdentifier
from test.elements.test_datasource_fixtures import (
    ELASTICSEARCH_DATASOURCE,
    INFLUXDB1_DATASOURCE,
    PROMETHEUS_DATASOURCE,
    TESTDATA_DATASOURCE,
)

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DatasourceTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned, dashboard_basic, folder_basic, docker_prometheus):  # noqa: ARG002
        self.grafana = grafana_provisioned
        self.dashboard = dashboard_basic
        self.folder = folder_basic
        self.datasource = self.grafana.datasource.create_datasource(PROMETHEUS_DATASOURCE)
        self.datasource_id = self.datasource["datasource"]["id"]
        self.datasource_uid = self.datasource["datasource"]["uid"]

    def test_get_datasource_by_id(self):
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing data sources by id, use uids instead.")

        result = self.grafana.datasource.get(DatasourceIdentifier(id=self.datasource_id))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_by_uid(self):
        result = self.grafana.datasource.get(DatasourceIdentifier(uid=self.datasource_uid))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_by_name(self):
        result = self.grafana.datasource.get(DatasourceIdentifier(name="Prometheus"))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_invalid(self):
        self.assertRaises(KeyError, lambda: self.grafana.datasource.get(DatasourceIdentifier()))

    def test_update_datasource_by_id(self):
        result = self.grafana.datasource.update_datasource(self.datasource_id, PROMETHEUS_DATASOURCE)
        self.assertEqual(result["datasource"]["type"], "prometheus")

    def test_update_datasource_by_uid(self):
        if Version(self.grafana.version) < Version("10"):
            pytest.skip("Grafana 9 and earlier do not support addressing data sources by uid.")
        result = self.grafana.datasource.update_datasource_by_uid(self.datasource_uid, PROMETHEUS_DATASOURCE)
        self.assertEqual(result["datasource"]["type"], "prometheus")

    def test_delete_datasource_by_id(self):
        result = self.grafana.datasource.delete_datasource_by_id(self.datasource_id)
        self.assertEqual(result, {"message": "Data source deleted"})

    def test_delete_datasource_by_uid(self):
        result = self.grafana.datasource.delete_datasource_by_uid(self.datasource_uid)
        result.pop("id", None)
        self.assertEqual(result, {"message": "Data source deleted"})

    def test_delete_datasource_by_name(self):
        result = self.grafana.datasource.delete_datasource_by_name("Prometheus")
        result.pop("id", None)
        self.assertEqual(result, {"message": "Data source deleted"})

    def test_find_datasource_by_name_success(self):
        result = self.grafana.datasource.find_datasource("Prometheus")
        self.assertEqual(result["type"], "prometheus")

    def test_find_datasource_by_name_not_existing(self):
        with self.assertRaises(GrafanaClientError) as excinfo:
            self.grafana.datasource.find_datasource("it_doesnot_exist")
        self.assertEqual(excinfo.exception.status_code, 404)
        self.assertEqual(excinfo.exception.message, "Client Error 404: Data source not found")

    def test_get_datasource_id_by_name(self):
        result = self.grafana.datasource.get_datasource_id_by_name("Prometheus")
        self.assertEqual(result["id"], self.datasource_id)

    def test_list_datasources(self):
        result = self.grafana.datasource.list_datasources()
        self.assertEqual(result[0]["type"], "prometheus")
        self.assertEqual(len(result), 1)

    def test_get_datasource_proxy_data_query_time(self):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query?query=up%7binstance%3d%22localhost:9090%22%7d&time=1644164339
        now = int(time.time())
        result = self.grafana.datasource.get_datasource_proxy_data(
            self.datasource_id,
            query_type="query",
            expr='up{instance="localhost:9090"}',
            time=now,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["result"]), 1)
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        self.assertEqual(result["data"]["result"][0]["value"], [now, "1"])

    def test_get_datasource_proxy_data_query_range(self):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query_range?query=up%7binstance%3d%22localhost:9090%22%7d&start=1644164339&end=1644164639&step=60
        now = int(time.time())
        result = self.grafana.datasource.get_datasource_proxy_data(
            self.datasource_id,
            query_type="query_range",
            expr='up{instance="localhost:9090"}',
            start=now - 300,
            end=now,
            step=60,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        self.assertEqual(len(result["data"]["result"][0]["values"]), 6)

    def test_get_datasource_proxy_data_failure(self):
        with self.assertRaises(KeyError) as ctx:
            self.grafana.datasource.get_datasource_proxy_data(
                self.datasource_id,
                query_type="foobar",
                expr='up{instance="localhost:9090"}',
                time=1644164339,
            )
        self.assertEqual(str(ctx.exception), "'Unknown or invalid query type: foobar'")

    def test_series(self):
        """
        http http://localhost:9090/api/v1/label/__name__/values
        """
        now = int(time.time())
        result = self.grafana.datasource.series(
            datasource_id=self.datasource_id,
            match="go_info",
            start=now - 300,
            end=now,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"][0]["job"], "prometheus")


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DatasourceInquiryTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_provisioned, docker_prometheus, docker_influxdb1, docker_elasticsearch):  # noqa: ARG002
        self.grafana = grafana_provisioned
        self.datasource_influxdb1 = self.grafana.datasource.create_datasource(INFLUXDB1_DATASOURCE)["datasource"]
        self.datasource_elasticsearch = self.grafana.datasource.create_datasource(ELASTICSEARCH_DATASOURCE)[
            "datasource"
        ]
        self.datasource_prometheus = self.grafana.datasource.create_datasource(PROMETHEUS_DATASOURCE)["datasource"]
        self.datasource_testdata = self.grafana.datasource.create_datasource(TESTDATA_DATASOURCE)["datasource"]

    def test_health(self):
        if Version(self.grafana.version) < Version("10"):
            pytest.skip("Data source health check endpoint is available in Grafana 10 and higher.")
        datasource_uid = self.datasource_testdata["uid"]
        result = self.grafana.datasource.health(datasource_uid)
        self.assertEqual(result["status"], "OK")

    def test_prometheus(self):
        response = self.grafana.datasource.smartquery(self.datasource_prometheus, "1+1")
        result = response["results"]["test"]
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(result["status"], 200)
        if Version(self.grafana.version) < Version("8"):
            self.assertEqual(result["series"][0]["points"][0][0], 2)
        else:
            self.assertEqual(result["frames"][0]["data"]["values"][1][0], 2)

    def test_influxdb_influxql(self):
        response = self.grafana.datasource.smartquery(
            self.datasource_influxdb1, "SHOW RETENTION POLICIES on _internal", attrs={"database": "foobar"}
        )
        result = response["results"][0]
        self.assertEqual(result["series"][0]["values"][0][0], "monitor")

    @pytest.mark.skip("Defunct: Currently fails with »bad request data«")
    def test_elasticsearch(self):
        datasource_id = self.datasource_elasticsearch["id"]
        _ = self.grafana.datasource.smartquery(
            self.datasource_elasticsearch, f"url:///datasources/proxy/{datasource_id}/bazqux/_mapping"
        )
        # TODO: Response payload not reflected and validated yet.

    def test_datasource_by_uid(self):
        datasource_uid = self.datasource_prometheus["uid"]
        response = self.grafana.datasource.smartquery(DatasourceIdentifier(uid=datasource_uid), "1+1")
        result = response["results"]["test"]
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(result["status"], 200)

    def test_unknown_access_type_failure(self):
        datasource = self.datasource_prometheus.copy()
        datasource["access"] = "__UNKNOWN__"
        self.assertRaises(NotImplementedError, lambda: self.grafana.datasource.smartquery(datasource, expression="1+1"))

    def test_empty_expression_failure(self):
        self.assertRaises(
            ValueError, lambda: self.grafana.datasource.smartquery(self.datasource_prometheus, expression=None)
        )

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_client_error_failure(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaClientError(status_code=400, response={}, message="Something failed")
        self.assertRaises(
            GrafanaClientError, lambda: self.grafana.datasource.smartquery(self.datasource_prometheus, expression="1+1")
        )

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_server_error_failure(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaServerError(
            status_code=500, response={}, message="Something serious failed"
        )
        self.assertRaises(
            GrafanaServerError, lambda: self.grafana.datasource.smartquery(self.datasource_prometheus, expression="1+1")
        )
