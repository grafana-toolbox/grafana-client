import unittest
from test.elements.test_datasource_fixtures import (
    DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
    ELASTICSEARCH_DATASOURCE,
    INFLUXDB1_DATASOURCE,
    PERMISSION_DATASOURCE,
    PROMETHEUS_DATA_RESPONSE,
    PROMETHEUS_DATASOURCE,
)
from unittest.mock import Mock, patch

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
)
from grafana_client.model import DatasourceIdentifier


class DatasourceTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_health(self, m):
        m.get(
            "http://localhost/api/datasources/uid/foobar/health",
            json={"message": "TwinMaker datasource successfully configured (For play.grafana.org)", "status": "OK"},
        )

        result = self.grafana.datasource.health("foobar")
        self.assertEqual(result["status"], "OK")

    @requests_mock.Mocker()
    def test_get_datasource_by_id(self, m):
        m.get(
            "http://localhost/api/datasources/42",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.get(DatasourceIdentifier(id="42"))
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_get_datasource_by_uid(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.get(DatasourceIdentifier(uid="h8KkCLt7z"))
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_get_datasource_by_name(self, m):
        m.get(
            "http://localhost/api/datasources/name/Prometheus",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.get(DatasourceIdentifier(name="Prometheus"))
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_get_datasource_invalid(self, m):
        self.assertRaises(KeyError, lambda: self.grafana.datasource.get(DatasourceIdentifier()))

    @requests_mock.Mocker()
    def test_create_datasource(self, m):
        m.post(
            "http://localhost/api/datasources",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.create_datasource(PROMETHEUS_DATASOURCE)
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_update_datasource(self, m):
        m.put(
            "http://localhost/api/datasources/42",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.update_datasource(42, PROMETHEUS_DATASOURCE)
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_update_datasource_by_uid(self, m):
        m.put(
            "http://localhost/api/datasources/uid/foo42",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.update_datasource_by_uid("foo42", PROMETHEUS_DATASOURCE)
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_delete_datasource_by_id(self, m):
        m.delete("http://localhost/api/datasources/42", json={"message": "Data source deleted"})

        result = self.grafana.datasource.delete_datasource_by_id(42)
        self.assertEqual(result, {"message": "Data source deleted"})

    @requests_mock.Mocker()
    def test_delete_datasource_by_uid(self, m):
        m.delete("http://localhost/api/datasources/uid/h8KkCLt7z", json={"message": "Data source deleted"})

        result = self.grafana.datasource.delete_datasource_by_uid("h8KkCLt7z")
        self.assertEqual(result, {"message": "Data source deleted"})

    @requests_mock.Mocker()
    def test_delete_datasource_by_name(self, m):
        m.delete("http://localhost/api/datasources/name/Prometheus", json={"message": "Data source deleted"})

        result = self.grafana.datasource.delete_datasource_by_name("Prometheus")
        self.assertEqual(result, {"message": "Data source deleted"})

    @requests_mock.Mocker()
    def test_enable_datasource_permissions(self, m):
        m.post(
            "http://localhost/api/datasources/42/enable-permissions", json={"message": "Datasource permissions enabled"}
        )

        result = self.grafana.datasource.enable_datasource_permissions(42)
        self.assertEqual(result, {"message": "Datasource permissions enabled"})

    @requests_mock.Mocker()
    def test_disable_datasource_permissions(self, m):
        m.post(
            "http://localhost/api/datasources/42/disable-permissions",
            json={"message": "Datasource permissions disabled"},
        )

        result = self.grafana.datasource.disable_datasource_permissions(42)
        self.assertEqual(result, {"message": "Datasource permissions disabled"})

    @requests_mock.Mocker()
    def test_get_datasource_permissions(self, m):
        m.get(
            "http://localhost/api/datasources/42/permissions",
            json=PERMISSION_DATASOURCE,
        )

        result = self.grafana.datasource.get_datasource_permissions(42)
        self.assertEqual(result["datasourceId"], 42)

    @requests_mock.Mocker()
    def test_add_datasource_permissions(self, m):
        m.post("http://localhost/api/datasources/42/permissions", json={"message": "Datasource permission added"})

        result = self.grafana.datasource.add_datasource_permissions(42, {"userId": 1, "permission": 1})
        self.assertEqual(result, {"message": "Datasource permission added"})

    @requests_mock.Mocker()
    def test_remove_datasource_permissions(self, m):
        m.delete("http://localhost/api/datasources/42/permissions/1", json={"message": "Datasource permission removed"})

        result = self.grafana.datasource.remove_datasource_permissions(42, 1)
        self.assertEqual(result, {"message": "Datasource permission removed"})

    @requests_mock.Mocker()
    def test_find_datasource(self, m):
        m.get(
            "http://localhost/api/datasources/name/Prometheus",
            json=PROMETHEUS_DATASOURCE,
        )

        result = self.grafana.datasource.find_datasource("Prometheus")
        self.assertEqual(result["type"], "prometheus")

    @requests_mock.Mocker()
    def test_find_datasource_not_existing(self, m):
        m.get(
            "http://localhost/api/datasources/name/it_doesnot_exist",
            json={"message": "Data source not found"},
            status_code=400,
        )

        with self.assertRaises(GrafanaBadInputError):
            self.grafana.datasource.find_datasource("it_doesnot_exist")

    @requests_mock.Mocker()
    def test_get_datasource_id_by_name(self, m):
        m.get("http://localhost/api/datasources/id/Prometheus", json={"id": 42})

        result = self.grafana.datasource.get_datasource_id_by_name("Prometheus")
        self.assertEqual(result["id"], 42)

    @requests_mock.Mocker()
    def test_list_datasources(self, m):
        m.get(
            "http://localhost/api/datasources",
            json=[PROMETHEUS_DATASOURCE],
        )

        result = self.grafana.datasource.list_datasources()
        self.assertEqual(result[0]["type"], "prometheus")
        self.assertEqual(len(result), 1)

    @requests_mock.Mocker()
    def test_get_datasource_proxy_data_query(self, m):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query?query=up%7binstance%3d%22localhost:9090%22%7d&time=1644164339
        m.post(
            "http://localhost/api/datasources/proxy/1/api/v1/query",
            json=PROMETHEUS_DATA_RESPONSE,
        )
        result = self.grafana.datasource.get_datasource_proxy_data(
            1,  # datasource_id
            query_type="query",
            expr='up{instance="localhost:9090"}',
            time=1644164339,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        self.assertEqual(len(result["data"]["result"][0]["values"]), 6)

    @requests_mock.Mocker()
    def test_get_datasource_proxy_data_query_range(self, m):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query_range?query=up%7binstance%3d%22localhost:9090%22%7d&start=1644164339&end=1644164639&step=60
        m.post(
            "http://localhost/api/datasources/proxy/1/api/v1/query_range",
            json=PROMETHEUS_DATA_RESPONSE,
        )
        result = self.grafana.datasource.get_datasource_proxy_data(
            1,  # datasource_id
            query_type="query_range",
            expr='up{instance="localhost:9090"}',
            start=1644164339,
            end=1644164639,
            step=60,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        self.assertEqual(len(result["data"]["result"][0]["values"]), 6)

    @requests_mock.Mocker()
    def test_get_datasource_proxy_data_failure(self, m):
        m.post(
            "http://localhost/api/datasources/proxy/1/api/v1/query",
            json=PROMETHEUS_DATA_RESPONSE,
        )
        with self.assertRaises(KeyError) as ctx:
            self.grafana.datasource.get_datasource_proxy_data(
                1,  # datasource_id
                query_type="foobar",
                expr='up{instance="localhost:9090"}',
                time=1644164339,
            )
        self.assertEqual(str(ctx.exception), "'Unknown or invalid query type: foobar'")

    @requests_mock.Mocker()
    def test_series(self, m):
        # TODO: Not sure if this emulates the right payloads.
        #       It has been copied from the other test functions above.
        m.post(
            "http://localhost/api/datasources/proxy/1/api/v1/series",
            json=PROMETHEUS_DATA_RESPONSE,
        )
        result = self.grafana.datasource.series(
            datasource_id=1,
            match="foo",
            start=1644164339,
            end=1644164639,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], "prometheus")
        self.assertEqual(len(result["data"]["result"][0]["values"]), 6)

    @requests_mock.Mocker()
    def test_query_with_datasource_prometheus(self, m):
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
        )
        datasource = PROMETHEUS_DATASOURCE.copy()
        response = self.grafana.datasource.smartquery(datasource, "1+1")
        self.assertEqual(response, DATAFRAME_RESPONSE_HEALTH_PROMETHEUS)

    @requests_mock.Mocker()
    def test_query_with_datasource_influxdb_influxql(self, m):
        m.post(
            "http://localhost/api/datasources/proxy/43/query",
            json={},
        )
        datasource = INFLUXDB1_DATASOURCE.copy()
        _ = self.grafana.datasource.smartquery(datasource, "SHOW RETENTION POLICIES on _internal", store="foobar")
        # TODO: No response payload yet.

    @requests_mock.Mocker()
    def test_query_with_datasource_elasticsearch(self, m):
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={},
        )
        datasource = ELASTICSEARCH_DATASOURCE.copy()
        _ = self.grafana.datasource.smartquery(
            datasource, "url:///datasources/proxy/44/bazqux/_mapping", store="bazqux"
        )
        # TODO: No response payload yet.

    @requests_mock.Mocker()
    def test_query_with_datasource_identifier(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
        )
        response = self.grafana.datasource.smartquery(DatasourceIdentifier(uid="h8KkCLt7z"), "1+1")
        self.assertEqual(response, DATAFRAME_RESPONSE_HEALTH_PROMETHEUS)

    def test_query_unknown_access_type_failure(self):
        datasource = PROMETHEUS_DATASOURCE.copy()
        datasource["access"] = "__UNKNOWN__"
        self.assertRaises(NotImplementedError, lambda: self.grafana.datasource.smartquery(datasource, expression="1+1"))

    def test_query_empty_expression_failure(self):
        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(ValueError, lambda: self.grafana.datasource.smartquery(datasource, expression=None))

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_query_client_error_failure(self, mock_get):

        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaClientError(status_code=400, response={}, message="Something failed")

        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(GrafanaClientError, lambda: self.grafana.datasource.smartquery(datasource, expression="1+1"))

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_query_server_error_failure(self, mock_get):

        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaServerError(
            status_code=500, response={}, message="Something serious failed"
        )

        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(GrafanaServerError, lambda: self.grafana.datasource.smartquery(datasource, expression="1+1"))
