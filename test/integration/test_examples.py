import dataclasses
import subprocess
import sys
from pathlib import Path
from typing import Callable

import pytest


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
    return "http://admin:admin@{docker_services.docker_ip}:{public_port}".format(**locals())


@pytest.fixture(scope="session")
def docker_cratedb(docker_services):
    """
    Provide CrateDB service.
    """
    docker_services.start("cratedb")
    public_port = docker_services.wait_for_service("cratedb", 4200)
    return "http://admin:admin@{docker_services.docker_ip}:{public_port}".format(**locals())


@pytest.fixture(scope="session")
def docker_influxdb1(docker_services):
    """
    Provide InfluxDB v1 service.
    """
    docker_services.start("influxdb1")
    public_port = docker_services.wait_for_service("influxdb1", 8086)
    return "http://admin:adminadmin@{docker_services.docker_ip}:{public_port}".format(**locals())


@pytest.fixture(scope="session")
def docker_influxdb2(docker_services):
    """
    Provide InfluxDB v2 service.
    """
    docker_services.start("influxdb2")
    public_port = docker_services.wait_for_service("influxdb2", 8086)
    return "http://admin:adminadmin@{docker_services.docker_ip}:{public_port}".format(**locals())


@pytest.fixture(scope="session")
def docker_elasticsearch(docker_services):
    """
    Provide Elasticsearch service.
    """
    docker_services.start("elasticsearch")
    public_port = docker_services.wait_for_service("elasticsearch", 9200)
    return "http://{docker_services.docker_ip}:{public_port}".format(**locals())


@dataclasses.dataclass
class DatabaseItem:
    type: str
    url: str
    fixture: Callable


database_trajectory = [
    DatabaseItem(type="cratedb", url="host.docker.internal:5433", fixture=docker_cratedb),
    DatabaseItem(type="elasticsearch", url="http://host.docker.internal:9200", fixture=docker_elasticsearch),
    DatabaseItem(type="influxdb", url="http://admin:adminadmin@host.docker.internal:18086", fixture=docker_influxdb1),
]
database_ids = [item.type for item in database_trajectory]


@pytest.mark.parametrize("database", database_trajectory, ids=database_ids)
def test_datasource_health_probe(docker_services, docker_grafana, database):  # noqa: ARG001
    database.fixture._get_wrapped_function()(docker_services)
    cmd = [
        sys.executable,
        "examples/datasource-health-probe.py",
        "--type",
        database.type,
        "--url",
        database.url,
    ]
    p = subprocess.run(cmd, env={"GRAFANA_URL": docker_grafana}, check=False)  # noqa: S603
    assert p.returncode == 0, f"Executing health probe failed. database={database.type}, url={database.url}"
