"""
About
=====
Knowledgebase module for filling the missing gaps to access the Grafana API
more efficiently.
"""
from grafana_client.model import DatasourceModel


def datasource_factory(datasource: DatasourceModel):
    """
    Create payload suitable for creating a Grafana data source item.

    Some data sources need additional configuration beyond the bare minimum
    attributes required by `DatasourceModel`.

    This is by far not a generic implementation. It merely satisfies the use
    case where Docker containers are started on localhost, like the data source
    health check demo program does. Many attributes are hardcoded to specific
    values. Additional parameterization work might make this function more
    generic in the future.

    TODO: Fill the gaps for other databases.
    """
    if datasource.type == "__NEVER__":
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
    elif datasource.type == "postgres":
        datasource.user = "postgres"
        datasource.jsonData = {
            "postgresVersion": 1200,
            "sslmode": "disable",
        }
    elif datasource.type == "prometheus":
        datasource.access = "proxy"
    elif datasource.type == "testdata":
        pass
    else:
        raise NotImplementedError(f"Unknown data source type: {datasource.type}")
    return datasource


def query_factory(datasource, expression: str):
    """
    Create payload suitable for running a query against a Grafana data source.

    TODO: Fill the gaps for other databases.
    """
    datasource_type = datasource["type"]
    if datasource_type == "__NEVER__":
        raise NotImplementedError("__NEVER__")
    elif datasource_type == "elasticsearch":
        query = expression
    elif datasource_type == "influxdb":
        dialect = datasource["jsonData"]["version"]
        if dialect == "InfluxQL":
            query = {
                "refId": "test",
                "datasource": {
                    "type": datasource["type"],
                    "uid": datasource.get("uid"),
                },
                "datasourceId": datasource.get("id"),
                "q": expression,
            }
        elif dialect == "Flux":
            query = {
                "refId": "test",
                "datasource": {
                    "type": datasource["type"],
                    "uid": datasource.get("uid"),
                },
                "datasourceId": datasource.get("id"),
                # "intervalMs": 60000,
                "maxDataPoints": 1,
                "query": expression,
            }
        else:
            raise KeyError(f"InfluxDB dialect '{dialect}' unknown")
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
            "refId": "test",
            "expr": expression,
            "instant": True,
            # "queryType": "timeSeriesQuery",
            # "exemplar": False,
            # "requestId": "0test",
            # "utcOffsetSec": 7200,
            # "legendFormat": "",
            # "interval": "",
            "datasource": {
                "type": datasource["type"],
                "uid": datasource.get("uid"),
            },
            "datasourceId": datasource.get("id"),
            # "intervalMs": 60000,
            "maxDataPoints": 1,
        }
    elif datasource_type == "testdata":
        query = expression
    else:
        raise NotImplementedError(f"Unknown data source type: {datasource_type}")
    return query


# Define health-check status queries for all database types.
# TODO: Fill the gaps for other databases.
HEALTHCHECK_EXPRESSION_MAP = {
    "elasticsearch": "url:///datasources/proxy/{datasource_id}/{database_name}/_mapping",
    "influxdb": "SHOW RETENTION POLICIES on _internal",
    "influxdb+influxql": "SHOW RETENTION POLICIES on _internal",
    "influxdb+flux": "buckets()",
    "postgres": "SELECT 1;",
    "prometheus": "1+1",
    "testdata": "url:///datasources/uid/{datasource_uid}",
}


def get_healthcheck_expression(datasource_type: str, datasource_dialect: str = None):
    """
    Produce data source health check query by database type.
    """
    if datasource_type == "influxdb" and datasource_dialect == "Flux":
        datasource_type = "influxdb+flux"
    if datasource_type not in HEALTHCHECK_EXPRESSION_MAP:
        raise NotImplementedError(f"Health check for datasource type {datasource_type} not implemented yet")
    return HEALTHCHECK_EXPRESSION_MAP[datasource_type]
