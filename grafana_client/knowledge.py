"""
About
=====
Knowledgebase module for filling the missing gaps to access the Grafana API
more efficiently.
"""
from datetime import datetime
from typing import Dict, Optional, Union

from grafana_client.model import DatasourceModel


def datasource_factory(datasource: DatasourceModel) -> DatasourceModel:
    """
    Create payload suitable for creating a Grafana data source item.

    Some data sources need additional configuration beyond the bare minimum
    attributes required by `DatasourceModel`.

    TODO: This is by far not a generic or complete implementation.
          It merely satisfies the use case where Docker containers are started
          on localhost, like the data source health check demo program does.
          Many attributes are hardcoded to specific values. Additional
          parameterization work might make this function more generic in the
          future.

    TODO: Complete the list for all popular databases.
    """
    if datasource.type == "__NEVER__":  # pragma:nocover
        raise NotImplementedError("__NEVER__")

    elif datasource.type == "cratedb":
        datasource.type = "postgres"
        datasource.user = "crate"
        datasource.jsonData = {
            "postgresVersion": 1200,
            "sslmode": "disable",
        }
    elif datasource.type == "elasticsearch":
        datasource.access = "proxy"
        datasource.database = "testdrive"
        datasource.jsonData = {
            "esVersion": "7.10.0",
            "timeField": "@timestamp",
        }
    elif datasource.type == "graphite":
        datasource.access = "proxy"
        datasource.jsonData = {
            "graphiteVersion": "1.1",
        }
    elif datasource.type in ["influxdb", "influxdb+influxql"]:
        datasource.type = "influxdb"
        datasource.access = "proxy"
        datasource.jsonData = {
            "httpMode": "POST",
            "version": "InfluxQL",
        }
    elif datasource.type in ["influxdb+flux"]:
        datasource.type = "influxdb"
        datasource.access = "proxy"
        datasource.jsonData = {
            "httpMode": "POST",
            "organization": "example",
            "version": "Flux",
        }
        datasource.secureJsonData = {
            "token": "admintoken",
        }
        datasource.secureJsonFields = {
            "token": False,
        }
    elif datasource.type == "jaeger":
        datasource.access = "proxy"
    elif datasource.type == "opentsdb":
        datasource.access = "proxy"
        datasource.jsonData = {
            "tsdbVersion": 3,
        }
    elif datasource.type == "loki":
        datasource.access = "proxy"
    elif datasource.type == "mssql":
        datasource.access = "proxy"
        datasource.database = "testdrive"
        datasource.user = "sa"
        datasource.jsonData = {
            "authenticationType": "SQL Server Authentication",
        }
        datasource.secureJsonData = {
            "password": "root123?",
        }
        datasource.secureJsonFields = {
            "password": False,
        }
    elif datasource.type == "mysql":
        datasource.user = "root"
        datasource.secureJsonData = {
            "password": "root",
        }
    elif datasource.type == "postgres":
        datasource.user = "postgres"
        datasource.jsonData = {
            "postgresVersion": 1200,
            "sslmode": "disable",
        }
    elif datasource.type == "prometheus":
        datasource.access = "proxy"
    elif datasource.type == "tempo":
        datasource.access = "proxy"
    elif datasource.type == "testdata":
        pass
    elif datasource.type == "zipkin":
        datasource.access = "proxy"
    else:
        raise NotImplementedError(f"Unknown data source type: {datasource.type}")
    return datasource


def query_factory(datasource, model: Optional[dict] = None, expression: Optional[str] = None) -> Union[Dict, str]:
    """
    Create payload suitable for running a query against a Grafana data source.

    TODO: This is by far not complete. It has to be made more elaborate in order
          to query different data source types.

    TODO: Complete the list for all popular databases.
    """

    model = model or {}
    if "query" not in model and expression:
        model["query"] = expression

    request = {
        "method": "POST",
        "data": None,
        "params": None,
    }
    attrs = None

    datasource_type = datasource["type"]
    expression = model.get("query")
    if expression is None:
        raise KeyError("query not set")
    if datasource_type == "__NEVER__":  # pragma:nocover
        raise NotImplementedError("__NEVER__")
    elif datasource_type == "elasticsearch":
        query = expression
    elif datasource_type == "fetzerch-sunandmoon-datasource":
        query = expression
    elif datasource_type == "grafana-simple-json-datasource":
        query = expression

    elif datasource_type == "graphite":
        query = {"target": expression, "from": "-5m", "until": "now", "format": "json", "maxDataPoints": 300}
        if "time_from" in model:
            query["from"] = model["time_from"]
        if "time_to" in model:
            query["until"] = model["time_to"]

        request["data"] = query

    elif datasource_type == "influxdb":
        dialect = datasource["jsonData"].get("version", "InfluxQL")
        query = {
            "refId": "test",
            # "datasource": {
            #     "type": datasource["type"],
            #     "uid": datasource.get("uid"),
            # },
            # "datasourceId": datasource.get("id"),
        }
        if dialect == "InfluxQL":
            query.update(
                {
                    "q": expression,
                }
            )
            # this drive the how timestamp are rendered in result (string by default, or in milliseconds ms)
            request["params"] = {"epoch": "ms"}
            if "database" in datasource:
                request["params"].update({"db": datasource["database"]})
            request["data"] = query

        elif dialect == "Flux":
            query = {
                "datasource": {
                    "type": datasource["type"],
                    "uid": datasource.get("uid"),
                },
                "datasourceId": datasource.get("id"),
                # "exemplar": False,
                "query": expression,
            }

            attrs = [
                {
                    "name": "intervalMs",
                    "default": 30000,
                },
                {
                    "name": "maxDataPoints",
                    "default": 1441,
                },
                {
                    "name": "refId",
                    "default": "test",
                },
            ]
        else:
            raise KeyError(f"InfluxDB dialect '{dialect}' unknown")

    elif datasource_type == "jaeger":
        query = {}

    elif datasource_type == "loki":
        query = {
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            # "exemplar": False,
            "expr": expression,
        }

        attrs = [
            {
                "name": "intervalMs",
                "default": 60000,
            },
            {
                "name": "legendFormat",
                "default": "",
            },
            {
                "name": "maxLines",
                "default": 1000,
            },
            {
                "name": "maxDataPoints",
                "default": 1441,
            },
            {
                "name": "queryType",
                "default": "range",
            },
            {
                "name": "refId",
                "default": "test",
            },
            {
                "name": "resolution",
                "default": 1,
            },
        ]

    elif datasource_type == "opentsdb":
        query = {}

    elif datasource_type in ("postgres", "mssql", "mysql"):
        query = {
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            "rawSql": expression,
        }
        attrs = [
            {
                "name": "format",
                "default": "time_series",
                "choices": ["time_series", "table"],
                # "version": "8.0.0"
            },
            {
                "name": "intervalMs",
                "default": 30000,
            },
            {
                "name": "maxDataPoints",
                "default": 1441,
            },
            {
                "name": "refId",
                "default": None,
            },
        ]

    elif datasource_type == "prometheus":
        query = {
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            # "exemplar": False,
            "expr": expression,
        }

        attrs = [
            {
                "name": "format",
                "default": "time_series",
                "choices": ["time_series", "table", "heatmap"],
                # "version": "8.0.0"
            },
            {
                "name": "instant",
                "default": False,
            },
            {
                "name": "interval",
                "default": "",
            },
            {
                "name": "intervalFactor",
                "default": None,
            },
            {
                "name": "intervalMs",
                "default": 30000,
            },
            {
                "name": "legendFormat",
                "default": "",
            },
            {
                "name": "maxDataPoints",
                "default": None,
            },
            {
                "name": "queryType",
                "default": "timeSeriesQuery",
            },
            {
                "name": "refId",
                "default": "test",
            },
            {
                "name": "requestId",
                "default": "0test",
            },
            {
                "name": "step",
                "default": 300,
            },
            {
                "name": "utcOffsetSec",
                "default": 0,
            },
        ]

    elif datasource_type == "simpod-json-datasource":
        query = expression
    elif datasource_type == "tempo":
        query = {}
    elif datasource_type == "testdata":
        query = expression
    elif datasource_type == "zipkin":
        query = {}
    else:
        raise NotImplementedError(f"Unknown data source type: {datasource_type}")

    if attrs is not None and query is not None and isinstance(query, dict):
        for attr in attrs:
            value = attr["default"]
            if attr["name"] in model:
                tmp_value = model[attr["name"]]
                if "choices" in attr:
                    if tmp_value in attr["choices"]:
                        value = tmp_value
                else:
                    value = tmp_value
            if value is not None:
                query[attr["name"]] = value

        if "time_from" not in model or "time_to" not in model:
            now = datetime.now()
            if "time_from" not in model:
                model["time_from"] = int(now.timestamp()) - 5 * 60
            if "time_to" not in model:
                model["time_to"] = int(now.timestamp())

        if "instant" in query and query["instant"]:
            model["time_from"] = model["time_to"]

        payload = {
            "queries": [query],
            "from": str(model["time_from"] * 1000),
            "to": str(model["time_to"] * 1000),
        }
        request["data"] = payload

    return request


# Define health-check status queries for all database types.
# TODO: Complete the list for all popular databases.
HEALTHCHECK_EXPRESSION_MAP = {
    "elasticsearch": "url:///datasources/proxy/{datasource_id}/{database_name}/_mapping",
    "fetzerch-sunandmoon-datasource": "url:///datasources/uid/{datasource_uid}",
    "grafana-simple-json-datasource": "url:///datasources/proxy/{datasource_id}",
    # From play.grafana.org, to explore Graphite datasource.
    "graphite": "random-walk.count;dc=asia-1;app=collector;server=000",
    "influxdb": "SHOW RETENTION POLICIES on _internal",
    "influxdb+influxql": "SHOW RETENTION POLICIES on _internal",
    "influxdb+flux": "buckets()",
    "jaeger": "url:///datasources/proxy/{datasource_id}/api/services",
    "loki": 'count_over_time({job=~".+"} [5m])',
    "mssql": "SELECT 1",
    "mysql": "SELECT 1",
    "opentsdb": "url:///datasources/proxy/{datasource_id}/api/suggest?type=metrics&q=cpu&max=100",
    "postgres": "SELECT 1",
    "prometheus": "1+1",
    "simpod-json-datasource": "url:///datasources/proxy/{datasource_id}",
    "tempo": "url:///datasources/proxy/{datasource_id}/api/echo",
    "testdata": "url:///datasources/uid/{datasource_uid}",
    "zipkin": "url:///datasources/proxy/{datasource_id}/api/v2/services",
}


def get_healthcheck_expression(datasource_type: str, datasource_dialect: str = None) -> str:
    """
    Produce data source health check query for corresponding database type.
    """
    if datasource_type == "influxdb" and datasource_dialect == "Flux":
        datasource_type = "influxdb+flux"
    if datasource_type not in HEALTHCHECK_EXPRESSION_MAP:
        raise NotImplementedError(f"Unknown data source type: {datasource_type}")
    return HEALTHCHECK_EXPRESSION_MAP[datasource_type]
