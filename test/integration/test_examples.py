import dataclasses
import os
import subprocess
import sys
from pathlib import Path

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):  # noqa: ARG001
    """
    Override this fixture in order to specify a custom location to your `docker-compose.yml`.
    """
    return [Path(__file__).parent / "docker-compose.yml"]


@pytest.fixture(scope="session")
def docker_services_project_name(pytestconfig):  # noqa: ARG001
    return "pytest_grafana-client"


@pytest.fixture(scope="session")
def docker_grafana(docker_services):
    """
    Provide Grafana service.
    """
    docker_services.start("grafana")
    public_port = docker_services.wait_for_service("grafana", 3000)
    return f"http://admin:admin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_cratedb(docker_services):
    """
    Provide CrateDB service.
    """
    docker_services.start("cratedb")
    public_port = docker_services.wait_for_service("cratedb", 4200)
    return f"http://admin:admin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_influxdb1(docker_services):
    """
    Provide InfluxDB v1 service.
    """
    docker_services.start("influxdb1")
    public_port = docker_services.wait_for_service("influxdb1", 8086)
    return f"http://admin:adminadmin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_influxdb2(docker_services):
    """
    Provide InfluxDB v2 service.
    """
    docker_services.start("influxdb2")
    public_port = docker_services.wait_for_service("influxdb2", 8086)
    return f"http://admin:adminadmin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_elasticsearch(docker_services):
    """
    Provide Elasticsearch service.
    """
    docker_services.start("elasticsearch")
    public_port = docker_services.wait_for_service("elasticsearch", 9200)
    return f"http://{docker_services.docker_ip}:{public_port}"


@dataclasses.dataclass
class DatabaseItem:
    type: str
    url: str
    fixture: str


database_trajectory = [
    DatabaseItem(type="cratedb", url="172.17.0.1:5433", fixture="docker_cratedb"),
    DatabaseItem(type="elasticsearch", url="http://172.17.0.1:9200", fixture="docker_elasticsearch"),
    DatabaseItem(type="influxdb", url="http://admin:adminadmin@172.17.0.1:18086", fixture="docker_influxdb1"),
]
database_ids = [item.type for item in database_trajectory]


@pytest.mark.parametrize("database", database_trajectory, ids=database_ids)
def test_datasource_health_probe(request, docker_grafana, database):

    # Skip health probe testing on Grafana 9.x and earlier.
    grafana = GrafanaApi.from_url(docker_grafana)
    grafana_version = grafana.version
    if Version(grafana_version) < Version("10"):
        pytest.skip(f"Skipping health probe testing on Grafana {grafana_version}")

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
