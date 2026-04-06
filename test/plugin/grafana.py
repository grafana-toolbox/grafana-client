"""
Grafana software test backbone, aka. `pytest-grafana`.
"""

import typing as t

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError

DataDictionary = t.Dict[str, t.Any]


@pytest.fixture(scope="session")
def docker_grafana(docker_services) -> str:
    """Provide Grafana service and return its URL."""
    docker_services.start("grafana")
    public_port = docker_services.wait_for_service("grafana", 3000)
    return f"http://admin:admin@{docker_services.docker_ip}:{public_port}"


@pytest.fixture(scope="session")
def grafana_api(docker_grafana) -> GrafanaApi:
    """Provide Grafana API instance connected to the service."""
    return GrafanaApi.from_url(docker_grafana)


@pytest.fixture()
def grafana_version(grafana_api: GrafanaApi) -> Version:
    """Inquire and provide current Grafana version."""
    return Version(grafana_api.version)


@pytest.fixture()
def datasource_testdata(grafana_api: GrafanaApi, reset_datasources) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana data source (TestData) for testing purposes."""
    from test.elements.test_datasource_fixtures import TESTDATA_DATASOURCE

    return grafana_api.datasource.create_datasource(TESTDATA_DATASOURCE)["datasource"]


@pytest.fixture()
def datasource_prometheus(grafana_api: GrafanaApi, reset_datasources) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana data source (Prometheus) for testing purposes."""
    from test.elements.test_datasource_fixtures import PROMETHEUS_DATASOURCE

    return grafana_api.datasource.create_datasource(PROMETHEUS_DATASOURCE)["datasource"]


@pytest.fixture()
def dashboard_id(grafana_dashboard: DataDictionary) -> int:
    """Provision Grafana dashboard and provide its ID."""
    return grafana_dashboard["id"]


@pytest.fixture()
def dashboard_uid(grafana_dashboard: DataDictionary) -> str:
    """Provision Grafana dashboard and provide its UID."""
    return grafana_dashboard["uid"]


@pytest.fixture(scope="function")
def grafana_dashboard(grafana_api: GrafanaApi, folder_uid: str) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana dashboard for testing purposes."""
    dashboard_uid = "cIBgcSjkk"
    return grafana_api.dashboard.update_dashboard(
        {
            "dashboard": {
                "uid": dashboard_uid,
                "title": "ProductionOverview",
                "tags": ["foobar", "bazqux"],
                "timezone": "browser",
            },
            "folderUid": folder_uid,
            "overwrite": True,
        }
    )


@pytest.fixture()
def folder_id(grafana_folder: DataDictionary) -> str:
    """Provision Grafana folder and provide its ID."""
    return grafana_folder["id"]


@pytest.fixture()
def folder_uid(grafana_folder: DataDictionary) -> str:
    """Provision Grafana folder and provide its UID."""
    return grafana_folder["uid"]


@pytest.fixture()
def folder_title(grafana_folder: DataDictionary) -> str:
    """Provision Grafana folder and provide its title."""
    return grafana_folder["title"]


@pytest.fixture(scope="function")
def grafana_folder(grafana_api: GrafanaApi, reset_folders_dashboards) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana folder for testing purposes."""
    folder_uid = "cfi05mqnc3k00a"
    try:
        return grafana_api.folder.create_folder(title="Testdrive", uid=folder_uid)

    # TODO: Currently needs to compensate for `Client Error 412: the folder
    #       has been changed by someone else`, indicating some collision in Grafana,
    #       or a timing problem within the test suite. Check why this happens.
    except GrafanaClientError as ex:
        if ex.status_code != 412:
            raise
    return grafana_api.folder.get_folder(uid=folder_uid)


@pytest.fixture(scope="function")
def grafana_team(grafana_api: GrafanaApi, reset_teams) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana team for testing purposes."""
    return grafana_api.teams.add_team({"name": "Foo Fighters"})


@pytest.fixture(scope="function")
def dashboard_folder_permissions(grafana_team) -> t.List[DataDictionary]:  # noqa: ARG001
    """Provide a set of dashboard or folder permissions."""
    team_id = grafana_team["teamId"]
    """
    items=[
        {"permission": "View"},
        {"permission": "Edit"},
    ],
    """
    return [
        {"role": "Viewer", "permission": 1},
        {"role": "Editor", "permission": 2},
        {"teamId": team_id, "permission": 1},
        {"userId": 1, "permission": 4},
    ]


@pytest.fixture(scope="function")
def user_id(grafana_user) -> int:
    """Provision Grafana user and provide its user ID."""
    return grafana_user["id"]


@pytest.fixture(scope="function")
def grafana_user(grafana_api: GrafanaApi, reset_user_model) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana user for testing purposes."""
    try:
        grafana_api.admin.create_user(
            {
                "login": "testdrive",
                "password": "secret",
                "OrgId": 1,
            }
        )
    except GrafanaClientError as err:
        if err.status_code != 412:
            raise
    return grafana_api.users.find_user("testdrive")


@pytest.fixture()
def organization_id(grafana_organization) -> str:
    """Provision Grafana organization and provide its ID."""
    return grafana_organization["orgId"]


@pytest.fixture()
def organization_name(grafana_organization) -> str:
    """Provision Grafana organization and provide its name."""
    return grafana_organization["name"]


@pytest.fixture(scope="function")
def grafana_organization(grafana_api: GrafanaApi, reset_user_model) -> DataDictionary:  # noqa: ARG001
    """Provision Grafana organization for testing purposes."""
    return grafana_api.organization.create_organization(organization="Testdrive Org.")


@pytest.fixture(scope="function")
def user_with_organization(grafana_api: GrafanaApi, grafana_user, organization_id) -> None:
    """Associate user with organization."""
    grafana_api.organizations.organization_user_add(
        organization_id=organization_id,
        user={"loginOrEmail": grafana_user["login"], "role": "Viewer"},
    )


@pytest.fixture()
def reset_organization_switch(grafana_api: GrafanaApi) -> t.Generator[None, None, None]:
    """Switch back to organization 1."""
    yield
    grafana_api.organizations.switch_organization(organization_id=1)


@pytest.fixture()
def reset_user_model(grafana_api: GrafanaApi, grafana_version: Version, reset_organization_switch, reset_teams) -> None:  # noqa: ARG001
    """Reset tokens, service accounts, users, teams, and organizations."""
    if grafana_version >= Version("9"):
        for account in grafana_api.serviceaccount.search_streaming():
            account_id = account["id"]
            for token in grafana_api.serviceaccount.get_tokens(account_id):
                grafana_api.serviceaccount.delete_token(account_id, token["id"])
            grafana_api.serviceaccount.delete(account_id)
    for user in grafana_api.users.search_users():
        if user["id"] != 1:
            grafana_api.admin.delete_user(user["id"])
    for org in grafana_api.organizations.list_organization():
        if org["id"] != 1:
            grafana_api.organizations.delete_organization(org["id"])
    grafana_api.organizations.update_organization(organization_id=1, organization={"name": "Main Org."})


@pytest.fixture()
def reset_teams(grafana_api: GrafanaApi) -> None:
    """Reset all teams."""
    for team in grafana_api.teams.search_teams():
        grafana_api.teams.delete_team(team["id"])


@pytest.fixture()
def reset_datasources(grafana_api: GrafanaApi, grafana_version: Version) -> None:
    """Reset all data sources."""
    for datasource in grafana_api.datasource.list_datasources():
        if grafana_version >= Version("7"):
            grafana_api.datasource.delete_datasource_by_uid(datasource["uid"])
        else:
            grafana_api.datasource.delete_datasource_by_id(datasource["id"])


@pytest.fixture()
def reset_folders_dashboards(grafana_api: GrafanaApi) -> None:
    """Reset all dashboards."""
    items = grafana_api.search.search_dashboards()
    dashboards = [item for item in items if item["type"] == "dash-db"]
    folders = [item for item in items if item["type"] == "dash-folder"]

    for item in dashboards + folders:
        try:
            if item["type"] == "dash-db":
                grafana_api.dashboard.delete_dashboard(item["uid"])
            elif item["type"] == "dash-folder":
                grafana_api.folder.delete_folder(item["uid"], force_delete_rules=True)
        except GrafanaClientError as ex:
            if ex.status_code != 404:
                raise


@pytest.fixture()
def reset_stars(grafana_api: GrafanaApi, grafana_version: Version, dashboard_uid: str) -> None:
    """Reset user dashboard stars."""
    if grafana_version >= Version("11"):
        grafana_api.user.unstar_dashboard(dashboard_uid)
