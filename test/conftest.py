import typing as t
from pathlib import Path

import pytest

pytest_plugins = [
    "test.plugin.datasource",
    "test.plugin.grafana",
]


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig) -> t.List[Path]:  # noqa: ARG001
    """
    Override this fixture in order to specify a custom location to your `docker-compose.yml`.
    """
    return [Path(__file__).parent / "compose.yml"]


@pytest.fixture(scope="session")
def docker_services_project_name(pytestconfig) -> str:  # noqa: ARG001
    return "pytest_grafana-client"
