import dataclasses
import os
import subprocess
import sys

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi

pytestmark = pytest.mark.integration


@dataclasses.dataclass
class DatabaseItem:
    type: str
    url: str
    fixture: str


# TODO: Add Prometheus and InfluxDB 2.
database_trajectory = [
    DatabaseItem(type="cratedb", url="172.17.0.1:5433", fixture="docker_cratedb"),
    DatabaseItem(type="elasticsearch", url="http://172.17.0.1:9200", fixture="docker_elasticsearch"),
    DatabaseItem(type="graphite", url="http://172.17.0.1:8080", fixture="docker_graphite"),
    DatabaseItem(type="influxdb", url="http://admin:adminadmin@172.17.0.1:18086", fixture="docker_influxdb1"),
    DatabaseItem(type="loki", url="http://172.17.0.1:3100", fixture="docker_loki"),
    DatabaseItem(type="mysql", url="172.17.0.1:3306", fixture="docker_mariadb"),
    DatabaseItem(type="postgres", url="172.17.0.1:5432", fixture="docker_postgresql"),
]
database_ids = [item.type for item in database_trajectory]


@pytest.mark.parametrize("database", database_trajectory, ids=database_ids)
def test_datasource_health_probe(request, docker_grafana, database):

    # Skip health probe testing on Grafana 9.x and earlier.
    grafana = GrafanaApi.from_url(docker_grafana)
    grafana_version = grafana.version
    if Version(grafana_version) < Version("10"):
        pytest.skip("Health probes are supported by Grafana 10 and higher.")

    if database.type == "elasticsearch" and Version(grafana_version) < Version("11"):
        pytest.skip("Health probes for Elasticsearch are supported by Grafana 11 and higher.")

    if database.type == "graphite" and Version(grafana_version) < Version("12"):
        pytest.skip("Health probes for Graphite are supported by Grafana 12 and higher.")

    # Spin up service.
    request.getfixturevalue(database.fixture)

    # Invoke probe.
    cmd = [
        sys.executable,
        "examples/datasource-health-probe.py",
        "--type",
        database.type,
        "--url",
        database.url,
    ]
    p = subprocess.run(  # noqa: S603
        cmd,
        env={**os.environ, "GRAFANA_URL": docker_grafana},
        check=False,
        text=True,
        timeout=120,
    )
    assert p.returncode == 0, f"Executing health probe failed. database={database.type}, url={database.url}"
