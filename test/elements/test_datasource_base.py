import os
import sys
import time
import unittest
from unittest.mock import Mock, patch

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaClientError,
    GrafanaServerError,
)
from grafana_client.model import DatasourceIdentifier
from test.elements.test_datasource_fixtures import (
    ELASTICSEARCH_DATASOURCE,
    INFLUXDB1_DATASOURCE,
    PROMETHEUS_DATASOURCE,
)

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DatasourceTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api: GrafanaApi,
        grafana_version: Version,
        docker_prometheus,  # noqa: ARG002
        datasource_prometheus,
    ):
        self.grafana = grafana_api
        self.grafana_version = grafana_version
        self.datasource_id = datasource_prometheus["id"]
        self.datasource_uid = datasource_prometheus.get("uid")

    def get_identifier(self):
        """Return data source identifier. Grafana 13 only understands UIDs."""
        if self.grafana.get_version() >= Version("13"):
            return {"datasource_uid": self.datasource_uid}
        else:
            return {"datasource_id": self.datasource_id}

    def test_get_datasource_by_id(self):
        if self.grafana.get_version() >= Version("12"):
            pytest.skip("Grafana 12 no longer supports accessing data sources by id, use uids instead.")

        result = self.grafana.datasource.get(DatasourceIdentifier(id=self.datasource_id))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_by_uid(self):
        if self.grafana_version < Version("7"):
            pytest.skip("Addressing data sources by UID only supported with Grafana 7 and higher.")
        result = self.grafana.datasource.get(DatasourceIdentifier(uid=self.datasource_uid))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_by_name(self):
        result = self.grafana.datasource.get(DatasourceIdentifier(name="Prometheus"))
        self.assertEqual(result["type"], "prometheus")

    def test_get_datasource_invalid(self):
        self.assertRaises(KeyError, lambda: self.grafana.datasource.get(DatasourceIdentifier()))

    def test_update_datasource_by_id(self):
        if self.grafana.version == "nightly" or self.grafana.get_version() >= Version("12.5"):
            pytest.skip("Grafana 12.5 stopped to support addressing data sources by ID.")
        result = self.grafana.datasource.update_datasource(self.datasource_id, PROMETHEUS_DATASOURCE)
        self.assertEqual(result["datasource"]["type"], "prometheus")

    def test_update_datasource_by_uid(self):
        if self.grafana_version < Version("7"):
            pytest.skip("Addressing data sources by UID only supported with Grafana 7 and higher.")
        if self.grafana.get_version() < Version("10"):
            pytest.skip("Grafana 9 and earlier do not support addressing data sources for update by UID.")
        result = self.grafana.datasource.update_datasource_by_uid(self.datasource_uid, PROMETHEUS_DATASOURCE)
        self.assertEqual(result["datasource"]["type"], "prometheus")

    def test_delete_datasource_by_id(self):
        if self.grafana.version == "nightly" or self.grafana.get_version() >= Version("12.5"):
            pytest.skip("Grafana 12.5 stopped to support addressing data sources by ID.")
        result = self.grafana.datasource.delete_datasource_by_id(self.datasource_id)
        self.assertEqual(result, {"message": "Data source deleted"})

    def test_delete_datasource_by_uid(self):
        if self.grafana_version < Version("7"):
            pytest.skip("Addressing data sources by UID only supported with Grafana 7 and higher.")
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
        self.assertEqual(404, excinfo.exception.status_code)
        self.assertIn("Data source not found", excinfo.exception.message)

    def test_get_datasource_id_by_name(self):
        result = self.grafana.datasource.get_datasource_id_by_name("Prometheus")
        self.assertEqual(result["id"], self.datasource_id)

    def test_list_datasources(self):
        result = self.grafana.datasource.list_datasources()
        self.assertEqual(result[0]["type"], "prometheus")
        self.assertEqual(len(result), 1)

    @pytest.mark.skipif("GITHUB_ACTIONS" in os.environ, reason="Not validated on GitHub Actions")
    def test_get_datasource_proxy_data_query_time(self):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query?query=up%7binstance%3d%22localhost:9090%22%7d&time=1644164339
        now = int(time.time())
        result = self.grafana.datasource.get_datasource_proxy_data(
            **self.get_identifier(),
            query_type="query",
            expr='up{instance="localhost:9090"}',
            time=now,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["data"]["result"]), 1)
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        ts, val = result["data"]["result"][0]["value"]
        self.assertEqual(val, "1")
        self.assertLessEqual(abs(float(ts) - now), 60)

    @pytest.mark.skipif("GITHUB_ACTIONS" in os.environ, reason="Not validated on GitHub Actions")
    def test_get_datasource_proxy_data_query_range(self):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query_range?query=up%7binstance%3d%22localhost:9090%22%7d&start=1644164339&end=1644164639&step=60
        now = int(time.time())
        result = self.grafana.datasource.get_datasource_proxy_data(
            **self.get_identifier(),
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

    @pytest.mark.skipif("GITHUB_ACTIONS" in os.environ, reason="Not validated on GitHub Actions")
    def test_series(self):
        """
        http http://localhost:9090/api/v1/label/__name__/values
        """
        if self.grafana.get_version() < Version("7"):
            pytest.skip("Inquiring data sources only supported with Grafana 7 and higher.")
        now = int(time.time())
        result = self.grafana.datasource.series(
            **self.get_identifier(),
            match="go_info",
            start=now - 300,
            end=now,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"][0]["job"], "prometheus")


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class DatasourceInquiryTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api,
        docker_prometheus,  # noqa: ARG002
        datasource_prometheus,
        datasource_testdata,
    ):
        self.grafana = grafana_api
        if self.grafana.get_version() < Version("7"):
            pytest.skip("Inquiring data sources only supported with Grafana 7 and higher.")
        self.datasource_prometheus = datasource_prometheus
        self.datasource_testdata = datasource_testdata
        self.datasource_testdata_uid = datasource_testdata.get("uid")

    def test_health(self):
        if self.grafana.get_version() < Version("10"):
            pytest.skip("Data source health check endpoint is available in Grafana 10 and higher.")
        result = self.grafana.datasource.health(self.datasource_testdata_uid)
        self.assertEqual(result["status"], "OK")

    def test_prometheus(self):
        response = self.grafana.datasource.smartquery(self.datasource_prometheus, "1+1")
        result = response["results"]["test"]
        if self.grafana.get_version() >= Version("9"):
            self.assertEqual(result["status"], 200)
        if self.grafana.get_version() < Version("8"):
            self.assertEqual(result["series"][0]["points"][0][0], 2)
        else:
            self.assertEqual(result["frames"][0]["data"]["values"][1][0], 2)

    def test_datasource_by_uid(self):
        datasource_uid = self.datasource_prometheus["uid"]
        response = self.grafana.datasource.smartquery(DatasourceIdentifier(uid=datasource_uid), "1+1")
        result = response["results"]["test"]
        if self.grafana.get_version() >= Version("9"):
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


@pytest.mark.skip(
    "Data querying with InfluxDB is currently defunct. "
    "Legacy data source API for InfluxDB no longer available for Grafana 12.5+. "
    "Also, while it works locally, it fails on GHA."
)
def test_influxdb_influxql(grafana_api, docker_influxdb1, reset_datasources):  # noqa: ARG001
    datasource_influxdb1 = grafana_api.datasource.create_datasource(INFLUXDB1_DATASOURCE)["datasource"]
    response = grafana_api.datasource.smartquery(
        datasource_influxdb1, "SHOW RETENTION POLICIES on _internal", attrs={"database": "foobar"}
    )
    result = response["results"][0]
    assert result["series"][0]["values"][0][0] == "monitor"


# FIXME: Elasticsearch data source currently fails with »bad request data«.
@pytest.mark.skip("FIXME: Elasticsearch data source currently fails with »bad request data«")
def test_elasticsearch(grafana_api, docker_elasticsearch, reset_datasources):  # noqa: ARG001
    datasource_elasticsearch = grafana_api.datasource.create_datasource(ELASTICSEARCH_DATASOURCE)["datasource"]
    datasource_id = datasource_elasticsearch["id"]
    grafana_api.datasource.smartquery(
        datasource_elasticsearch, f"url:///datasources/proxy/{datasource_id}/bazqux/_mapping"
    )
    # TODO: Response payload not reflected and validated yet.
