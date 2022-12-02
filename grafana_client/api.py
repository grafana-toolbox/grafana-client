import logging
import os
import warnings
from functools import lru_cache as memoized
from typing import Tuple, Union
from urllib.parse import parse_qs, urlparse

import requests
import requests.auth
from urllib3.exceptions import InsecureRequestWarning

from .client import GrafanaClient
from .elements import (
    Admin,
    Alerting,
    AlertingProvisioning,
    Annotations,
    Dashboard,
    DashboardVersions,
    Datasource,
    Folder,
    Health,
    Notifications,
    Organization,
    Organizations,
    Search,
    Snapshots,
    Teams,
    User,
    Users,
)
from .util import as_bool

logger = logging.getLogger(__name__)


class GrafanaApi:
    def __init__(
        self,
        auth=None,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        verify=True,
        timeout=5.0,
        user_agent: str = None,
    ):
        self.client = GrafanaClient(
            auth,
            host=host,
            port=port,
            url_path_prefix=url_path_prefix,
            protocol=protocol,
            verify=verify,
            timeout=timeout,
            user_agent=user_agent,
        )
        self.url = None
        self.admin = Admin(self.client)
        self.alerting = Alerting(self.client)
        self.alertingprovisioning = AlertingProvisioning(self.client)
        self.dashboard = Dashboard(self.client)
        self.dashboard_versions = DashboardVersions(self.client)
        self.datasource = Datasource(self.client, self)
        self.folder = Folder(self.client)
        self.health = Health(self.client)
        self.organization = Organization(self.client)
        self.organizations = Organizations(self.client, self)
        self.search = Search(self.client)
        self.user = User(self.client)
        self.users = Users(self.client)
        self.teams = Teams(self.client)
        self.annotations = Annotations(self.client)
        self.snapshots = Snapshots(self.client)
        self.notifications = Notifications(self.client)

    def connect(self):
        try:
            grafana_info = self.health.check()
        except requests.exceptions.ConnectionError as ex:
            logger.critical(f"Unable to connect to Grafana at {self.url or self.client.url_host}: {ex}")
            raise
        logger.info(f"Connected to Grafana at {self.url}: {grafana_info}")
        return grafana_info

    @property
    @memoized(maxsize=1)
    def version(self):
        grafana_info = self.health.check()
        version = grafana_info["version"]
        logger.info(f"Inquired Grafana version: {version}")
        return version

    @classmethod
    def from_url(cls, url: str = None, credential: Union[str, Tuple[str, str], requests.auth.AuthBase] = None):
        """
        Factory method to create a `GrafanaApi` instance from a URL.

        Accepts an optional credential, which is either an authentication
        token, or a tuple of (username, password).
        """

        # Sanity checks and defaults.
        if url is None:
            url = "http://admin:admin@localhost:3000"

        if credential is not None and not isinstance(credential, (str, Tuple, requests.auth.AuthBase)):
            raise TypeError(f"Argument 'credential' has wrong type: {type(credential)}")

        original_url = url
        url = urlparse(url)

        # Use username and password from URL.
        if credential is None and url.username:
            credential = (url.username, url.password)

        # Optionally turn off SSL verification.
        verify = as_bool(parse_qs(url.query).get("verify", [True])[0])
        if verify is False:
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)

        grafana = cls(
            credential,
            protocol=url.scheme,
            host=url.hostname,
            port=url.port,
            url_path_prefix=url.path.lstrip("/"),
            verify=verify,
        )
        grafana.url = original_url

        return grafana

    @classmethod
    def from_env(cls):
        """
        Factory method to create a `GrafanaApi` instance from environment variables.
        """
        return cls.from_url(url=os.environ.get("GRAFANA_URL"), credential=os.environ.get("GRAFANA_TOKEN"))
