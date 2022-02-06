import json
import unittest

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
    GrafanaUnauthorizedError,
)


class DatasourceTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")


    @requests_mock.Mocker()
    def test_find_datasource(self, m):
        m.get(
            "http://localhost/api/datasources/name/Prometheus",
            json={
                "id":1,
                "uid":"h8KkCLt7z",
                "orgId":1,
                "name":"Prometheus",
                "type":"prometheus",
                "typeName":"Prometheus",
                "typeLogoUrl":"public/app/plugins/datasource/prometheus/img/prometheus_logo.svg",
                "access":"proxy",
                "url":"http://localhost:9090",
                "password":"",
                "user":"",
                "database":"",
                "basicAuth": False,
                "isDefault": True,
                "jsonData":{
                    "httpMethod":"POST"
                },
                "readOnly": False
            }
        )

        result = self.grafana.datasource.find_datasource('Prometheus')
        self.assertEqual(result["type"], 'prometheus')

    @requests_mock.Mocker()
    def test_find_datasource_not_existing(self, m):
        m.get(
            "http://localhost/api/datasources/name/it_doesnot_exist",
            json= {"message": "Data source not found"},
            status_code=400
        )

        with self.assertRaises(GrafanaBadInputError):
            result = self.grafana.datasource.find_datasource('it_doesnot_exist')


    @requests_mock.Mocker()
    def test_get_datasource_id_by_name(self, m):
        m.get(
            "http://localhost/api/datasources/id/Prometheus",
            json={"id": 1}
        )

        result = self.grafana.datasource.get_datasource_id_by_name('Prometheus')
        self.assertEqual(result["id"], 1)


    @requests_mock.Mocker()
    def test_list_datasources(self, m):
        m.get(
            "http://localhost/api/datasources",
            json=[
                {
                    "id":1,
                    "uid":"h8KkCLt7z",
                    "orgId":1,
                    "name":"Prometheus",
                    "type":"prometheus",
                    "typeName":"Prometheus",
                    "typeLogoUrl":"public/app/plugins/datasource/prometheus/img/prometheus_logo.svg",
                    "access":"proxy",
                    "url":"http://localhost:9090",
                    "password":"",
                    "user":"",
                    "database":"",
                    "basicAuth": False,
                    "isDefault": True,
                    "jsonData":{
                        "httpMethod":"POST"
                    },
                    "readOnly": False
                }
            ],
        )

        result = self.grafana.datasource.list_datasources()
        self.assertEqual(result[0]["type"], 'prometheus')
        self.assertEqual(len(result), 1)

    @requests_mock.Mocker()
    def test_get_datasource_proxy_data(self, m):
        # http://localhost:3000/api/datasources/proxy/1/api/v1/query_range?query=up%7binstance%3d%22localhost:9090%22%7d&start=1644164339&end=1644164639&step=60 
        m.get(
            "http://localhost/api/datasources/proxy/1/api/v1/query_range",
            json={
                "status": "success",
                "data": {
                    "resultType": "matrix",
                    "result":[
                        {
                            "metric":{
                                "__name__":"up",
                                "instance":"localhost:9090",
                                "job":"prometheus"
                            },
                            "values":[
                                [1644164339,"1"],
                                [1644164399,"1"],
                                [1644164459,"1"],
                                [1644164519,"1"],
                                [1644164579,"1"],
                                [1644164639,"1"]
                            ]
                        }
                    ]
                }
            }
        )
        result = self.grafana.datasource.get_datasource_proxy_data(
            1, # datasource_id
            query_type='query_range',
            expr="up{instance=\"localhost:9090\"}",
            start=1644164339,
            end=1644164639,
            step=60,
        )
        self.assertEqual(result["status"], 'success')
        self.assertEqual(result["data"]["result"][0]["metric"]["job"], 'prometheus')
        self.assertEqual(len(result["data"]["result"][0]["values"]), 6)
