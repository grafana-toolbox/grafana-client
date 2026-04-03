import typing as t
from pathlib import Path

import pytest

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError


@pytest.fixture(scope="session")
def docker_compose_files(pytestconfig) -> t.List[Path]:  # noqa: ARG001
    """
    Override this fixture in order to specify a custom location to your `docker-compose.yml`.
    """
    return [Path(__file__).parent / "compose.yml"]


@pytest.fixture(scope="session")
def docker_services_project_name(pytestconfig) -> str:  # noqa: ARG001
    return "pytest_grafana-client"


@pytest.fixture(scope="session")
def docker_grafana(docker_services) -> str:
    """
    Provide Grafana service.
    """
    docker_services.start("grafana")
    public_port = docker_services.wait_for_service("grafana", 3000)
    return f"http://admin:admin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def grafana_api(docker_grafana) -> GrafanaApi:
    """
    Provide Grafana API instance.
    """
    return GrafanaApi.from_url(docker_grafana)


@pytest.fixture(scope="function")
def dashboard_basic(grafana_api):
    dashboard_uid = "cIBgcSjkk"
    try:
        grafana_api.dashboard.delete_dashboard(dashboard_uid)
    except GrafanaClientError as ex:
        if ex.status_code != 404:
            raise
    return grafana_api.dashboard.update_dashboard(
        {
            "dashboard": {
                "uid": dashboard_uid,
                "title": "Production Overview",
                "tags": ["foobar", "bazqux"],
                "timezone": "browser",
            },
            "overwrite": True,
        }
    )


@pytest.fixture(scope="function")
def folder_basic(grafana_api):
    folder_uid = "cfi05mqnc3k00a"
    try:
        grafana_api.folder.delete_folder(folder_uid)
    except GrafanaClientError as ex:
        if ex.status_code != 404:
            raise
    return grafana_api.folder.create_folder(title="Testdrive", uid=folder_uid)


@pytest.fixture(scope="session")
def team_basic(grafana_api):
    try:
        grafana_api.teams.add_team({"name": "Foo Fighters"})
    except GrafanaClientError as ex:
        if ex.status_code != 409:
            raise


@pytest.fixture(scope="function")
def grafana_provisioned(grafana_api, dashboard_basic, folder_basic, team_basic) -> GrafanaApi:  # noqa: ARG001
    """
    Provide Grafana API instance.
    """
    return grafana_api
