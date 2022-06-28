"""
About
=====
Knowledgebase module for filling the missing gaps to access the Grafana API
more efficiently.
"""
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


def query_factory(datasource, expression: str, store: Optional[str] = None) -> Union[Dict, str]:
    """
    Create payload suitable for running a query against a Grafana data source.

    TODO: This is by far not complete. It has to be made more elaborate in order
          to query different data source types.

    TODO: Complete the list for all popular databases.
    """
    datasource_type = datasource["type"]
    if datasource_type == "__NEVER__":  # pragma:nocover
        raise NotImplementedError("__NEVER__")
    elif datasource_type == "elasticsearch":
        query = expression
    elif datasource_type == "fetzerch-sunandmoon-datasource":
        query = expression
    elif datasource_type == "grafana-simple-json-datasource":
        query = expression
    elif datasource_type == "graphite":
        query = {"target": "constantLine(100)", "from": "-1h", "until": "now", "format": "json", "maxDataPoints": 300}
    elif datasource_type == "influxdb":
        dialect = datasource["jsonData"].get("version", "InfluxQL")
        query = {
            "refId": "test",
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
        }
        if dialect == "InfluxQL":
            query.update(
                {
                    "q": expression,
                }
            )
        elif dialect == "Flux":
            query.update(
                {
                    # "intervalMs": 60000,
                    "maxDataPoints": 1,
                    "query": expression,
                }
            )
        else:
            raise KeyError(f"InfluxDB dialect '{dialect}' unknown")
    elif datasource_type == "jaeger":
        query = {}
    elif datasource_type == "loki":
        query = {}
    elif datasource_type == "mssql":
        query = {
            "refId": "test",
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            "format": "table",
            "rawSql": expression,
        }
    elif datasource_type == "mysql":
        query = {
            "refId": "test",
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            "format": "table",
            "rawSql": expression,
        }
    elif datasource_type == "opentsdb":
        query = {}
    elif datasource_type == "postgres":
        query = {
            "refId": "test",
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            "format": "table",
            "rawSql": expression,
        }
    elif datasource_type == "prometheus":
        query = {
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            # "exemplar": False,
            "expr": expression,
            # "format": "time_series",
            # "instant": True,
            # "interval": "",
            # "intervalFactor": 10,
            # "intervalMs": 30000,
            # "legendFormat": "",
            # "maxDataPoints": 100,
            # "metric": store,
            # "queryType": "timeSeriesQuery",
            "refId": "test",
            "requestId": "0test",
            # "step": 300,
            # "utcOffsetSec": 7200,
        }
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
    return query


# Define health-check status queries for all database types.
# TODO: Complete the list for all popular databases.
HEALTHCHECK_EXPRESSION_MAP = {
    "elasticsearch": "url:///datasources/proxy/{datasource_id}/{database_name}/_mapping",
    "fetzerch-sunandmoon-datasource": "url:///datasources/uid/{datasource_uid}",
    "grafana-simple-json-datasource": "url:///datasources/proxy/{datasource_id}",
    "graphite": "None",  # TODO: Allow real None's.
    "influxdb": "SHOW RETENTION POLICIES on _internal",
    "influxdb+influxql": "SHOW RETENTION POLICIES on _internal",
    "influxdb+flux": "buckets()",
    "jaeger": "url:///datasources/proxy/{datasource_id}/api/services",
    "loki": "url:///datasources/{datasource_id}/resources/labels?start=1656274994383000000&end=1656275594383000000",
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
