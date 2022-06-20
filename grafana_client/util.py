import logging
import sys
import warnings
from urllib.parse import parse_qs, urlparse

from urllib3.exceptions import InsecureRequestWarning


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-35s] %(levelname)-7s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def grafana_client_factory(grafana_url, grafana_token=None):
    """
    From `grafana-wtf`.
    """
    url = urlparse(grafana_url)

    # Grafana API Key auth
    if grafana_token:
        auth = grafana_token

    # HTTP basic auth
    else:
        username = url.username or "admin"
        password = url.password or "admin"
        auth = (username, password)

    verify = as_bool(parse_qs(url.query).get("verify", [True])[0])
    if verify is False:
        warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    from grafana_client import GrafanaApi

    grafana = GrafanaApi(
        auth,
        protocol=url.scheme,
        host=url.hostname,
        port=url.port,
        url_path_prefix=url.path.lstrip("/"),
        verify=verify,
    )

    return grafana


def as_bool(value: str) -> bool:
    """
    Given a string value that represents True or False, returns the Boolean equivalent.
    Heavily inspired from distutils strtobool.

    From `isort`: https://github.com/PyCQA/isort/blob/5.10.1/isort/settings.py#L915-L922
    """

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    _STR_BOOLEAN_MAPPING = {
        "y": True,
        "yes": True,
        "t": True,
        "on": True,
        "1": True,
        "true": True,
        "n": False,
        "no": False,
        "f": False,
        "off": False,
        "0": False,
        "false": False,
    }
    try:
        return _STR_BOOLEAN_MAPPING[value.lower()]
    except KeyError:
        raise ValueError(f"invalid truth value {value}")
