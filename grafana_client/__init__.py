try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:  # pragma:nocover
    from importlib_metadata import PackageNotFoundError, version

from .api import AsyncGrafanaApi, GrafanaApi  # noqa:E402,F401
from .client import HeaderAuth, TokenAuth  # noqa:E402,F401

__appname__ = "grafana-client"

try:
    __version__ = version(__appname__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
