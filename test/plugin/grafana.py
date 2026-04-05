import typing as t

import pytest

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError


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
def datasource_testdata(grafana_api):
    from test.elements.test_datasource_fixtures import TESTDATA_DATASOURCE

    try:
        grafana_api.datasource.create_datasource(TESTDATA_DATASOURCE)
    except GrafanaClientError as ex:
        if ex.status_code != 409:
            raise


@pytest.fixture()
def dashboard_uid() -> str:
    return "cIBgcSjkk"


@pytest.fixture(scope="function")
def dashboard_basic(grafana_api, dashboard_uid):
    try:
        grafana_api.dashboard.delete_dashboard(dashboard_uid)
    except GrafanaClientError as ex:
        if ex.status_code != 404:
            raise
    return grafana_api.dashboard.update_dashboard(
        {
            "dashboard": {
                "uid": dashboard_uid,
                "title": "ProductionOverview",
                "tags": ["foobar", "bazqux"],
                "timezone": "browser",
            },
            "overwrite": True,
        }
    )


@pytest.fixture()
def folder_uid() -> str:
    return "cfi05mqnc3k00a"


@pytest.fixture(scope="function")
def folder_basic(grafana_api, folder_uid) -> t.Dict[str, str]:
    try:
        grafana_api.folder.delete_folder(folder_uid)
    except GrafanaClientError as ex:
        if ex.status_code != 404:
            raise
    return grafana_api.folder.create_folder(title="Testdrive", uid=folder_uid)


@pytest.fixture(scope="function")
def team_basic(grafana_api):
    try:
        grafana_api.teams.add_team({"name": "Foo Fighters"})
    except GrafanaClientError as ex:
        if ex.status_code != 409:
            raise


@pytest.fixture(scope="function")
def user_testdrive(grafana_api, organization_testdrive):
    try:
        return grafana_api.admin.create_user(
            {
                "login": "testdrive",
                "password": "secret",
                "OrgId": organization_testdrive["orgId"],
            }
        )
    except GrafanaClientError as err:
        if err.status_code == 412:
            return grafana_api.users.find_user("testdrive")
        else:
            raise


@pytest.fixture()
def organization_name() -> str:
    return "Testdrive Org."


@pytest.fixture(scope="function")
def organization_testdrive(grafana_api, organization_name: str):
    try:
        return grafana_api.organization.create_organization(organization=organization_name)
    except GrafanaClientError as err:
        if err.status_code == 412:
            return grafana_api.organization.find_organization(organization_name)
        else:
            raise


@pytest.fixture(scope="function")
def reset_grafana(grafana_api):

    # Reset context.
    grafana_api.organizations.switch_organization(organization_id=1)

    # Reset folders and dashboards.
    for folder in grafana_api.folder.get_all_folders():
        try:
            grafana_api.folder.delete_folder(folder["uid"], force_delete_rules=True)
        except GrafanaClientError as ex:
            if ex.status_code != 404:
                raise

    # Reset data sources.
    for datasource in grafana_api.datasource.list_datasources():
        grafana_api.datasource.delete_datasource_by_uid(datasource["uid"])

    # Reset users and organizations.
    for user in grafana_api.users.search_users():
        if user["id"] != 1:
            grafana_api.admin.delete_user(user["id"])
    for org in grafana_api.organizations.list_organization():
        if org["id"] != 1:
            grafana_api.organizations.delete_organization(org["id"])
    grafana_api.organizations.update_organization(organization_id=1, organization={"name": "Main Org."})


# ruff: disable[ARG001]
@pytest.fixture(scope="function")
def grafana_provisioned(
    grafana_api,
    reset_grafana,
    datasource_testdata,
    dashboard_basic,
    folder_basic,
    team_basic,
) -> GrafanaApi:
    """
    Provide Grafana API instance.
    """
    return grafana_api


# ruff: enable[ARG001]
