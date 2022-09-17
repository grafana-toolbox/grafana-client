import unittest
from test.elements.test_datasource_fixtures import (
    DATAFRAME_RESPONSE_EMPTY,
    DATAFRAME_RESPONSE_HEALTH_PROMETHEUS,
    DATAFRAME_RESPONSE_HEALTH_SELECT1,
    DATAFRAME_RESPONSE_INVALID,
    ELASTICSEARCH_DATASOURCE,
    GRAPHITE_DATASOURCE,
    INFLUXDB1_DATASOURCE,
    JAEGER_DATASOURCE,
    LOKI_DATASOURCE,
    MSSQL_DATASOURCE,
    MYSQL_DATASOURCE,
    OPENTSDB_DATASOURCE,
    POSTGRES_DATASOURCE,
    PROMETHEUS_DATASOURCE,
    SIMPLE_JSON_DATASOURCE,
    SIMPOD_JSON_DATASOURCE,
    SUNANDMOON_DATASOURCE,
    SUNANDMOON_DATASOURCE_INCOMPLETE,
    TEMPO_DATASOURCE,
    TESTDATA_DATASOURCE,
    ZIPKIN_DATASOURCE,
)

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError, GrafanaServerError
from grafana_client.model import DatasourceHealthResponse, DatasourceIdentifier


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
    def test_health_check_jaeger_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/DbtFe237k",
            json=JAEGER_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/53/api/services",
            json={"data": ["jaeger-query"], "total": 1, "limit": 0, "offset": 0, "errors": None},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="DbtFe237k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="DbtFe237k",
                type="jaeger",
                success=True,
                status="OK",
                message="['jaeger-query']",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_jaeger_error_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/DbtFe237k",
            json=JAEGER_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/53/api/services",
            json={
                "data": ["jaeger-query"],
                "total": 1,
                "limit": 0,
                "offset": 0,
                "errors": [{"code": 418, "message": "foobar"}],
            },
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="DbtFe237k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="DbtFe237k",
                type="jaeger",
                success=False,
                status="ERROR",
                message="[{'code': 418, 'message': 'foobar'}]",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_loki_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/vCyglaq7z",
            json=LOKI_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/54/resources/labels",
            json={"status": "success", "data": ["__name__"]},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="vCyglaq7z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="vCyglaq7z",
                type="loki",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_loki_error_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/vCyglaq7z",
            json=LOKI_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/54/resources/labels",
            json={"message": "Failed to call resource", "traceID": "00000000000000000000000000000000"},
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="vCyglaq7z"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="vCyglaq7z",
                type="loki",
                success=False,
                status="ERROR",
                message="Failed to call resource",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_mssql(self, m):
        m.get(
            "http://localhost/api/datasources/uid/0pueH83nz",
            json=MSSQL_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json=DATAFRAME_RESPONSE_HEALTH_SELECT1,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="0pueH83nz"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="0pueH83nz",
                type="mssql",
                success=True,
                status="OK",
                message="SELECT 1",
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
    def test_health_check_tempo_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/aTk86s3nk",
            json=TEMPO_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/55/api/echo",
            headers={"Content-Type": "text/plain"},
            text="echo",
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="aTk86s3nk"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="aTk86s3nk",
                type="tempo",
                success=True,
                status="OK",
                message="Success",
                duration=None,
                response=None,
            ),
        )

    @requests_mock.Mocker()
    def test_health_check_tempo_error_response_failure(self, m):
        m.get(
            "http://localhost/api/datasources/uid/aTk86s3nk",
            json=TEMPO_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/55/api/echo",
            status_code=502,
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="aTk86s3nk"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="aTk86s3nk",
                type="tempo",
                success=False,
                status="ERROR",
                message="Server Error 502: ",
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
    def test_health_check_zipkin_success(self, m):
        m.get(
            "http://localhost/api/datasources/uid/3sXIv8q7k",
            json=ZIPKIN_DATASOURCE,
        )
        m.get(
            "http://localhost/api/datasources/proxy/57/api/v2/services",
            json=[],
        )
        response = self.grafana.datasource.health_check(DatasourceIdentifier(uid="3sXIv8q7k"))
        response.duration = None
        response.response = None
        self.assertEqual(
            response,
            DatasourceHealthResponse(
                uid="3sXIv8q7k",
                type="zipkin",
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
                message="FATAL: Unable to decode result from dictionary-type response. "
                "TypeError: Invalid response format",
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
        Here: A response with an empty "results" slot.
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
    def test_health_check_zdummy_void_response_failure(self, m):
        """
        This is not a test for a real `postgres` data source.
        It only exercises a specific response shape.
        Here: An absolute empty (void) response.
        """
        m.get(
            "http://localhost/api/datasources/uid/v2KYBt37k",
            json=POSTGRES_DATASOURCE,
        )
        m.post(
            "http://localhost/api/ds/query",
            json={},
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
                message="Response lacks expected keys 'results' or 'data'",
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
                message="FATAL: Unknown response type '<class 'str'>'. Expected: dictionary or list.",
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
                message="Unknown: Client Error 404: Something failed. "
                "Response: {'status': 'ERROR', 'message': 'Something failed'}",
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
