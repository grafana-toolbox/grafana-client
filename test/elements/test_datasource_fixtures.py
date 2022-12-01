from copy import deepcopy

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

JAEGER_DATASOURCE = {
    "id": 53,
    "uid": "DbtFe237k",
    "name": "Jaeger",
    "type": "jaeger",
    "access": "proxy",
}

LOKI_DATASOURCE = {
    "id": 54,
    "uid": "vCyglaq7z",
    "name": "Loki",
    "type": "loki",
    "access": "proxy",
}

MSSQL_DATASOURCE = {
    "id": 56,
    "uid": "0pueH83nz",
    "name": "MSSQL",
    "type": "mssql",
    "access": "proxy",
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

TEMPO_DATASOURCE = {
    "id": 55,
    "uid": "aTk86s3nk",
    "name": "Tempo",
    "type": "tempo",
    "access": "proxy",
}

TESTDATA_DATASOURCE = {
    "id": 45,
    "uid": "439fngqr2",
    "name": "Testdata",
    "type": "testdata",
    "access": "proxy",
}

ZIPKIN_DATASOURCE = {
    "id": 57,
    "uid": "3sXIv8q7k",
    "name": "Zipkin",
    "type": "zipkin",
    "access": "proxy",
}

PERMISSION_DATASOURCE = {
    "datasourceId": 42,
    "enabled": True,
    "permissions": [
        {
            "id": 42,
            "datasourceId": 42,
            "teamId": 32,
            "teamAvatarUrl": "/avatar/c5e5ac09a2af1dec9a828d002c6bd4ea",
            "team": "a12",
            "permission": 1,
            "permissionName": "Query",
            "isManaged": True,
            "created": "2022-11-30T15:57:58Z",
            "updated": "2022-11-30T15:57:58Z",
        }
    ],
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
