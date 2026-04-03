import pytest

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaTimeoutError


def test_grafana_client_timeout(docker_grafana):
    grafana = GrafanaApi.from_url(docker_grafana, timeout=0.0001)
    with pytest.raises(GrafanaTimeoutError) as excinfo:
        grafana.folder.get_all_folders()
    assert excinfo.match("timed out")
