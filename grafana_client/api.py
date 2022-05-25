from .client import GrafanaClient
from .elements import (
    Admin,
    Annotations,
    Dashboard,
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
    ):
        self.client = GrafanaClient(
            auth,
            host=host,
            port=port,
            url_path_prefix=url_path_prefix,
            protocol=protocol,
            verify=verify,
            timeout=timeout,
        )
        self.admin = Admin(self.client)
        self.dashboard = Dashboard(self.client)
        self.datasource = Datasource(self.client)
        self.folder = Folder(self.client)
        self.health = Health(self.client)
        self.organization = Organization(self.client)
        self.organizations = Organizations(self.client)
        self.search = Search(self.client)
        self.user = User(self.client)
        self.users = Users(self.client)
        self.teams = Teams(self.client)
        self.annotations = Annotations(self.client)
        self.snapshots = Snapshots(self.client)
        self.notifications = Notifications(self.client)
