import unittest
from copy import deepcopy
from unittest.mock import Mock, patch

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
)
from grafana_client.model import DatasourceHealthResponse, DatasourceIdentifier

ELASTICSEARCH_DATASOURCE = {
    "id": 44,
    "uid": "34inf2sdc",
    "name": "Elasticsearch",
    "type": "elasticsearch",
    "access": "proxy",
    "database": "bazqux",
    "url": "http://localhost:9200",
    "jsonData": {
        "esVersion": "7.10.0",
        "timeField": "@timestamp",
    },
}

GRAPHITE_DATASOURCE = {
    "id": 48,
    "uid": "wr47rz34e",
    "name": "Graphite",
    "type": "graphite",
    "access": "proxy",
}

INFLUXDB1_DATASOURCE = {
    "id": 43,
    "uid": "9ac78sdc2",
    "name": "InfluxDB",
    "type": "influxdb",
    "access": "proxy",
    "url": "http://localhost:8086",
    "jsonData": {"httpMode": "POST", "version": "InfluxQL"},
}

MYSQL_DATASOURCE = {
    "id": 51,
    "uid": "7CpzLp37z",
    "name": "MariaDB",
    "type": "mysql",
    "access": "proxy",
    "url": "localhost:3306",
}

OPENTSDB_DATASOURCE = {
    "id": 51,
    "uid": "hkuk5h3nk",
    "name": "OpenTSDB",
    "type": "opentsdb",
    "access": "proxy",
}

POSTGRES_DATASOURCE = {
    "id": 50,
    "uid": "v2KYBt37k",
    "name": "PostgreSQL",
    "type": "postgres",
    "access": "proxy",
    "url": "localhost:5432",
    "jsonData": {
        "postgresVersion": 1200,
        "sslmode": "disable",
    },
}

PROMETHEUS_DATASOURCE = {
    "id": 42,
    "uid": "h8KkCLt7z",
    "orgId": 1,
    "name": "Prometheus",
    "type": "prometheus",
    "typeName": "Prometheus",
    "typeLogoUrl": "public/app/plugins/datasource/prometheus/img/prometheus_logo.svg",
    "access": "proxy",
    "url": "http://localhost:9090",
    "password": "",
    "user": "",
    "database": "",
    "basicAuth": False,
    "isDefault": True,
    "jsonData": {"httpMethod": "POST"},
    "readOnly": False,
}

SIMPLE_JSON_DATASOURCE = {
    "id": 47,
    "uid": "rw783ds3e",
    "name": "SimpleJson",
    "type": "grafana-simple-json-datasource",
    "access": "proxy",
}

SIMPOD_JSON_DATASOURCE = {
    "id": 49,
    "uid": "oie238af3",
    "name": "SimpodJson",
    "type": "simpod-json-datasource",
    "access": "proxy",
}

SUNANDMOON_DATASOURCE = {
    "id": 46,
    "uid": "239fasva4",
    "name": "SunAndMoon",
    "type": "fetzerch-sunandmoon-datasource",
    "access": "proxy",
    "jsonData": {
        "latitude": 42.42,
        "longitude": 84.84,
    },
}
SUNANDMOON_DATASOURCE_INCOMPLETE = deepcopy(SUNANDMOON_DATASOURCE)
del SUNANDMOON_DATASOURCE_INCOMPLETE["jsonData"]["latitude"]

TESTDATA_DATASOURCE = {
    "id": 45,
    "uid": "439fngqr2",
    "name": "Testdata",
    "type": "testdata",
    "access": "proxy",
}


PROMETHEUS_DATA_RESPONSE = {
    "status": "success",
    "data": {
        "resultType": "matrix",
        "result": [
            {
                "metric": {"__name__": "up", "instance": "localhost:9090", "job": "prometheus"},
                "values": [
                    [1644164339, "1"],
                    [1644164399, "1"],
                    [1644164459, "1"],
                    [1644164519, "1"],
                    [1644164579, "1"],
                    [1644164639, "1"],
                ],
            }
        ],
    },
}


DATAFRAME_RESPONSE_EMPTY = {"results": {"test": {"frames": []}}}
DATAFRAME_RESPONSE_INVALID = {"results": {"test": {"frames": "foobar"}}}
DATAFRAME_RESPONSE_HEALTH_SELECT1 = {
    "results": {"test": {"frames": [{"schema": {"meta": {"executedQueryString": "SELECT 1"}}}]}}
}

DATAFRAME_RESPONSE_HEALTH_PROMETHEUS = {
    "results": {
        "test": {
            "frames": [
                {
                    "schema": {
                        "name": "1+1",
                        "refId": "test",
                        "meta": {
                            "type": "timeseries-many",
                            "custom": {"resultType": "matrix"},
                            "executedQueryString": "Expr: 1+1\nStep: 15s",
                        },
                        "fields": [
                            {
                                "name": "Time",
                                "type": "time",
                                "typeInfo": {"frame": "time.Time"},
                                "config": {"interval": 15000},
                            },
                            {
                                "name": "Value",
                                "type": "number",
                                "typeInfo": {"frame": "float64", "nullable": True},
                                "labels": {},
                                "config": {"displayNameFromDS": "1+1"},
                            },
                        ],
                    },
                    "data": {"values": [[0], [2]]},
                }
            ]
        }
    }
}


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
        m.get(
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
        m.get(
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
    def test_query_with_datasource_prometheus(self, m):
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
        )
        datasource = PROMETHEUS_DATASOURCE.copy()
        response = self.grafana.datasource.query(datasource, "1+1")
        self.assertEqual(response, DATAFRAME_RESPONSE_HEALTH_PROMETHEUS)

    @requests_mock.Mocker()
    def test_query_with_datasource_influxdb_influxql(self, m):
        m.post(
            "http://localhost/api/datasources/proxy/43/query",
            json={},
        )
        datasource = INFLUXDB1_DATASOURCE.copy()
        response = self.grafana.datasource.query(datasource, "SHOW RETENTION POLICIES on _internal", store="foobar")
        # TODO: No response payload yet.

    @requests_mock.Mocker()
    def test_query_with_datasource_elasticsearch(self, m):
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={},
        )
        datasource = ELASTICSEARCH_DATASOURCE.copy()
        response = self.grafana.datasource.query(
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
        response = self.grafana.datasource.query(DatasourceIdentifier(uid="h8KkCLt7z"), "1+1")
        self.assertEqual(response, DATAFRAME_RESPONSE_HEALTH_PROMETHEUS)

    def test_query_unknown_access_type_failure(self):
        datasource = PROMETHEUS_DATASOURCE.copy()
        datasource["access"] = "__UNKNOWN__"
        self.assertRaises(NotImplementedError, lambda: self.grafana.datasource.query(datasource, expression="1+1"))

    def test_query_empty_expression_failure(self):
        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(ValueError, lambda: self.grafana.datasource.query(datasource, expression=None))

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_query_client_error_failure(self, mock_get):

        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaClientError(status_code=400, response={}, message="Something failed")

        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(GrafanaClientError, lambda: self.grafana.datasource.query(datasource, expression="1+1"))

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_query_server_error_failure(self, mock_get):

        mock_get.return_value = Mock()
        mock_get.return_value.side_effect = GrafanaServerError(
            status_code=500, response={}, message="Something serious failed"
        )

        datasource = PROMETHEUS_DATASOURCE.copy()
        self.assertRaises(GrafanaServerError, lambda: self.grafana.datasource.query(datasource, expression="1+1"))


class DatasourceHealthCheckTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_health_check_access_type_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )

        datasource = PROMETHEUS_DATASOURCE.copy()
        datasource["access"] = "__UNKNOWN__"
        self.assertRaises(NotImplementedError, lambda: self.grafana.datasource.health_check(datasource))

    @requests_mock.Mocker()
    def test_health_check_elasticsearch_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/34inf2sdc",
            json=ELASTICSEARCH_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={"bazqux": {"mappings": {"properties": "something"}}},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="34inf2sdc"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="34inf2sdc",
                type="elasticsearch",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_elasticsearch_empty_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/34inf2sdc",
            json=ELASTICSEARCH_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="34inf2sdc"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="34inf2sdc",
                type="elasticsearch",
                success=False,
                status="ERROR",
                message="No response for database 'bazqux'",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_elasticsearch_incomplete_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/34inf2sdc",
            json=ELASTICSEARCH_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={"bazqux": {}},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="34inf2sdc"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="34inf2sdc",
                type="elasticsearch",
                success=False,
                status="ERROR",
                message="Invalid response. KeyError: 'mappings'",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_elasticsearch_error_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/34inf2sdc",
            json=ELASTICSEARCH_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={"error": "This failed!", "status": 400},
            status_code=400,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="34inf2sdc"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="34inf2sdc",
                type="elasticsearch",
                success=False,
                status="ERROR",
                message="This failed!",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_elasticsearch_error_response_with_root_cause_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/34inf2sdc",
            json=ELASTICSEARCH_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/44/bazqux/_mapping",
            json={"error": {"root_cause": [{"type": "foo", "reason": "bar"}]}, "status": 400},
            status_code=400,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="34inf2sdc"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="34inf2sdc",
                type="elasticsearch",
                success=False,
                status="ERROR",
                message="Status: 400. Type: foo. Reason: bar",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_graphite_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/wr47rz34e",
            json=GRAPHITE_DATASOURCE,
        )
        m.post(
            "http://localhost/api/datasources/proxy/48/render",
            json=[{"target": "", "tags": {}, "datapoints": []}],
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="wr47rz34e"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="wr47rz34e",
                type="graphite",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_graphite_empty_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/wr47rz34e",
            json=GRAPHITE_DATASOURCE,
        )
        m.post(
            "http://localhost/api/datasources/proxy/48/render",
            json=[],
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="wr47rz34e"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="wr47rz34e",
                type="graphite",
                success=False,
                status="ERROR",
                message="Invalid response. IndexError: list index out of range",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_influxdb1(self, m):
        m.get(
            "http://localhost/api/datasources/uid/9ac78sdc2",
            json=INFLUXDB1_DATASOURCE,
        )
        m.post(
            "http://localhost/api/datasources/proxy/43/query",
            json={
                "results": [
                    {
                        "statement_id": 0,
                        "series": [
                            {
                                "columns": ["name", "duration", "shardGroupDuration", "replicaN", "default"],
                                "values": [["monitor", "168h0m0s", "24h0m0s", 1, True]],
                            }
                        ],
                    }
                ]
            },
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="9ac78sdc2"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="9ac78sdc2",
                type="influxdb",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_mysql(self, m):
        m.get(
            "http://localhost/api/datasources/uid/7CpzLp37z",
            json=MYSQL_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_SELECT1,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="7CpzLp37z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="7CpzLp37z",
                type="mysql",
                success=True,
                status="OK",
                message="SELECT 1",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_opentsdb(self, m):
        m.get(
            "http://localhost/api/datasources/uid/hkuk5h3nk",
            json=OPENTSDB_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/51/api/suggest",
            json="",
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="hkuk5h3nk"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="hkuk5h3nk",
                type="opentsdb",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_postgres(self, m):
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_SELECT1,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=True,
                status="OK",
                message="SELECT 1",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_prometheus_healthy_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="h8KkCLt7z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="h8KkCLt7z",
                type="prometheus",
                success=True,
                status="OK",
                message="Expr: 1+1\nStep: 15s",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_prometheus_empty_dataframe_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_EMPTY,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="h8KkCLt7z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="h8KkCLt7z",
                type="prometheus",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_prometheus_invalid_dataframe_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_INVALID,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="h8KkCLt7z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="h8KkCLt7z",
                type="prometheus",
                success=False,
                status="ERROR",
                message="FATAL: Unable to decode result from dictionary-type response. "
                "TypeError: DataFrame response detected, but 'frames' is not a list",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_simplejson(self, m):
        m.get(
            "http://localhost/api/datasources/uid/rw783ds3e",
            json=SIMPLE_JSON_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/47",
            json={"results": {"test": {"error": "Resource not found: /metadata"}}},
            status_code=404,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="rw783ds3e"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="rw783ds3e",
                type="grafana-simple-json-datasource",
                success=False,
                status="ERROR",
                message="Resource not found: /metadata",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_simpod_json(self, m):
        m.get(
            "http://localhost/api/datasources/uid/oie238af3",
            json=SIMPOD_JSON_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/49",
            json={"results": [{"statement_id": "ID", "series": []}]},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="oie238af3"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="oie238af3",
                type="simpod-json-datasource",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_sunandmoon_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/239fasva4",
            json=SUNANDMOON_DATASOURCE,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="239fasva4"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="239fasva4",
                type="fetzerch-sunandmoon-datasource",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_sunandmoon_incomplete_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/239fasva4",
            json=SUNANDMOON_DATASOURCE_INCOMPLETE,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="239fasva4"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="239fasva4",
                type="fetzerch-sunandmoon-datasource",
                success=False,
                status="ERROR",
                message="Invalid response. KeyError: 'latitude'",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_testdata(self, m):
        m.get(
            "http://localhost/api/datasources/uid/439fngqr2",
            json=TESTDATA_DATASOURCE,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="439fngqr2"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="439fngqr2",
                type="testdata",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zdict_valid_response_success(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The new DataFrame dictionary-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": {"test": {"refId": "foobar", "meta": {"executedQueryString": "ALIVE?"}}}},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=True,
                status="OK",
                message="ALIVE?",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zdict_incomplete_response_success(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The new DataFrame dictionary-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": {"test": {"refId": "foobar"}}},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zdict_incomplete_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The new DataFrame dictionary-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": {"test": {}}},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="FATAL: Unable to decode result from dictionary-type response. TypeError: Invalid response format",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zlist_error_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The previous list-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": [{"error": "This failed!"}]},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="This failed!",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zlist_incomplete_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The previous list-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": [{}]},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="FATAL: Unable to decode result from list-type response. KeyError: 'statement_id'",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zlist_empty_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: The previous list-type response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": []},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="FATAL: Unable to decode result from list-type response. IndexError: list index out of range",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zzdummy_invalid_type_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: A response with an invalid data type.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"results": "WRONG!"},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="FATAL: Unknown response type '<class 'str'>' from data source type 'postgres'",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_zzdummy_exception_without_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: A response with an invalid data type.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=None,
            status_code=400,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="v2KYBt37k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="v2KYBt37k",
                type="postgres",
                success=False,
                status="ERROR",
                message="Bad Input: ``",
                duration=None,
                response=None,
            ),
        )


class DatasourceHealthInquiryTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_health_inquiry_native_prometheus_success(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"type": "unknown"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en/health",
            json={"status": "OK", "message": "Excellent!"},
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="39mf288en",
                type="unknown",
                success=True,
                status="OK",
                message="Excellent!",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_native_prometheus_failure(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"type": "unknown"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en/health",
            json={"status": "ERROR", "message": "No way!"},
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="39mf288en",
                type="unknown",
                success=False,
                status="ERROR",
                message="No way!",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_native_unknown_error_400(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"type": "unknown"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en/health",
            json={"status": "ERROR", "message": "Something failed"},
            status_code=400,
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="39mf288en",
                type="unknown",
                success=False,
                status="ERROR",
                message="Something failed",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_native_unknown_error_418(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"type": "unknown"},
        )
        m.get(
            "http://localhost/api/datasources/uid/39mf288en/health",
            json={"status": "ERROR", "message": "Something failed"},
            status_code=418,
        )
        with self.assertRaises(GrafanaClientError) as ctx:
            self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        self.assertEqual(str(ctx.exception), "Client Error 418: Something failed")

    @requests_mock.Mocker()
    def test_health_inquiry_native_prometheus_error_404(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"status": "ERROR", "message": "Something failed"},
            status_code=404,
        )
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z/health",
            json={"status": "ERROR", "message": "Something failed"},
            status_code=404,
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="h8KkCLt7z")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="h8KkCLt7z",
                type="prometheus",
                success=False,
                status="ERROR",
                message="Unknown: Client Error 404: Something failed. Response: {'status': 'ERROR', 'message': 'Something failed'}",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_native_prometheus_error_500(self, m):
        m.get(
            "http://localhost/api/health",
            json={"commit": "14e988bd22", "database": "ok", "version": "9.0.1"},
        )
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z",
            json=PROMETHEUS_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={"status": "ERROR", "message": "Something failed"},
            status_code=500,
        )
        m.get(
            "http://localhost/api/datasources/uid/h8KkCLt7z/health",
            json={"status": "ERROR", "message": "Something failed", "code": "foobar"},
            status_code=500,
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="h8KkCLt7z")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="h8KkCLt7z",
                type="prometheus",
                success=False,
                status="FATAL",
                message="[foobar] GrafanaServerError: Server Error 500: Something failed",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_response_404(self, m):
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"status": "FATAL", "message": "Not found"},
            status_code=404,
        )
        response = self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="39mf288en",
                type=None,
                success=False,
                status="ERROR",
                message="Not found",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_inquiry_response_418(self, m):
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"status": "FATAL", "message": "Bad request"},
            status_code=418,
        )
        self.assertRaises(
            GrafanaClientError, lambda: self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        )

    @requests_mock.Mocker()
    def test_health_inquiry_response_500(self, m):
        m.get(
            "http://localhost/api/datasources/uid/39mf288en",
            json={"status": "FATAL", "message": "Server failed"},
            status_code=500,
        )
        self.assertRaises(
            GrafanaServerError, lambda: self.grafana.datasource.health_inquiry(datasource_uid="39mf288en")
        )
