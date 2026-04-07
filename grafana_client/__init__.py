try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # ty: ignore[unresolved-import]

__appname__ = "grafana-client"

try:
    __version__ = version(__appname__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from grafana_client.api import AsyncGrafanaApi, GrafanaApi  # noqa: E402,F401
from grafana_client.client import HeaderAuth, TokenAuth  # noqa: E402,F401
