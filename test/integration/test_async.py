import asyncio

import pytest

from grafana_client import AsyncGrafanaApi
from grafana_client.client import GrafanaServerError

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_basic_async_client(docker_grafana, dashboard_basic):

    # Connect to Grafana.
    grafana = AsyncGrafanaApi.from_url(docker_grafana)
    await grafana.connect()
    version = await grafana.version
    assert version != "" and "." in version

    # Provision dashboard and verify.
    dashboard_uid = dashboard_basic["uid"]
    dashboard = await grafana.dashboard.update_dashboard(
        {
            "dashboard": {
                "uid": dashboard_uid,
                "title": "Production Overview",
                "tags": ["foobar"],
                "timezone": "browser",
            },
            "overwrite": True,
        }
    )
    dashboard = await grafana.dashboard.get_dashboard(dashboard["uid"])
    assert isinstance(dashboard, dict)
    assert dashboard["meta"]["version"] >= 1
    assert dashboard["dashboard"]["tags"] == ["foobar"]

    # Non-blocking I/O semi-parallel fetch.
    tasks = []
    dashboards = await grafana.search.search_dashboards(type_="dash-db")
    for dashboard in dashboards:
        tasks.append(grafana.dashboard.get_dashboard(dashboard["uid"]))
    results = await asyncio.gather(*tasks)
    assert len(results) >= 1
    assert all(isinstance(r, dict) and list(r.keys()) for r in results)


@pytest.mark.asyncio
async def test_exception_async_client(docker_grafana):
    grafana = AsyncGrafanaApi.from_url(docker_grafana)
    await grafana.version

    with pytest.raises(GrafanaServerError) as exc:
        await grafana.admin.change_user_password(0, "impossible")
    assert exc.match("Server Error 500: (Failed to update user password|Could not read user from database)")
