from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig):  # noqa: ARG001
    """
    Override this fixture in order to specify a custom location to your `docker-compose.yml`.
    """
    return [Path(__file__).parent / "compose.yml"]


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
