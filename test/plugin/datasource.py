import time

import pytest

from test.util import port_is_up


@pytest.fixture(scope="session")
def docker_cratedb(docker_services):
    """
    Provide CrateDB service.
    """
    docker_services.start("cratedb")
    public_port = docker_services.wait_for_service("cratedb", 4200)
    return f"http://admin:admin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_elasticsearch(docker_services):
    """
    Provide Elasticsearch service.
    """
    docker_services.start("elasticsearch")
    public_port = docker_services.wait_for_service("elasticsearch", 9200)
    return f"http://{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_graphite(docker_services):
    """
    Provide Graphite StatsD service.
    """
    docker_services.start("graphite")
    public_port = docker_services.wait_for_service("graphite", 8080)
    return f"http://{docker_services.docker_ip}:{public_port}"


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
def docker_loki(docker_services):
    """
    Provide Loki service.
    """
    docker_services.start("loki")
    public_port = docker_services.wait_for_service("loki", 3100)
    time.sleep(7)
    return f"http://{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_mariadb(docker_services):
    """
    Provide MariaDB service.
    """
    docker_services.start("mariadb")
    public_port = docker_services.port_for("mariadb", 3306)
    docker_services.wait_until_responsive(
        check=lambda: port_is_up(docker_services.docker_ip, public_port),
        timeout=30,
        pause=1,
    )
    time.sleep(5)
    return f"{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_postgresql(docker_services):
    """
    Provide PostgreSQL service.
    """
    docker_services.start("postgresql")
    public_port = docker_services.port_for("postgresql", 5432)
    docker_services.wait_until_responsive(
        check=lambda: port_is_up(docker_services.docker_ip, public_port),
        timeout=30,
        pause=1,
    )
    time.sleep(2)
    return f"{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def docker_prometheus(docker_services):
    """
    Provide Prometheus service.
    """
    docker_services.start("prometheus")
    public_port = docker_services.port_for("prometheus", 9090)
    docker_services.wait_until_responsive(
        check=lambda: port_is_up(docker_services.docker_ip, public_port),
        timeout=30,
        pause=1,
    )
    return f"{docker_services.docker_ip}:{public_port}"
