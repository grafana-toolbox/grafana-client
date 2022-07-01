from .base import Base


class DashboardVersions(Base):
    """
    About
    =====
    Access Grafana "Dashboard Versions" API.

    Reference
    =========
    https://grafana.com/docs/grafana/latest/developers/http_api/dashboard_versions/
    """

    def __init__(self, client):
        super(DashboardVersions, self).__init__(client)
        self.client = client

    @staticmethod
    def api_path(dashboard_id: int = None, dashboard_uid: str = None):
        if dashboard_id is not None:
            path = f"/dashboards/id/{dashboard_id}"
        elif dashboard_uid is not None:
            path = f"/dashboards/uid/{dashboard_uid}"
        else:
            raise LookupError("Either dashboard_id or dashboard_uid is required")
        return path

    def get_dashboard_versions(
        self, dashboard_id: int = None, dashboard_uid: str = None, limit: int = None, start: int = None
    ):
        api_path = self.api_path(dashboard_id=dashboard_id, dashboard_uid=dashboard_uid)
        dashboard_versions_path = f"{api_path}/versions"

        query_args = {}
        if limit is not None:
            query_args["limit"] = limit
        if start is not None:
            query_args["start"] = start

        r = self.client.GET(dashboard_versions_path, data=query_args)
        return r

    def get_dashboard_versions_by_id(self, dashboard_id: int = None, limit: int = None, start: int = None):
        return self.get_dashboard_versions(dashboard_id=dashboard_id, limit=limit, start=start)

    def get_dashboard_versions_by_uid(self, dashboard_uid: str = None, limit: int = None, start: int = None):
        return self.get_dashboard_versions(dashboard_uid=dashboard_uid, limit=limit, start=start)

    def get_dashboard_version(self, dashboard_id: int = None, dashboard_uid: str = None, version_id: int = None):
        api_path = self.api_path(dashboard_id=dashboard_id, dashboard_uid=dashboard_uid)
        dashboard_version_path = f"{api_path}/versions/{version_id}"

        if version_id is None:
            raise LookupError("version_id is required")

        r = self.client.GET(dashboard_version_path)
        return r

    def get_dashboard_version_by_id(self, dashboard_id: int = None, version_id: int = None):
        return self.get_dashboard_version(dashboard_id=dashboard_id, version_id=version_id)

    def get_dashboard_version_by_uid(self, dashboard_uid: int = None, version_id: int = None):
        return self.get_dashboard_version(dashboard_uid=dashboard_uid, version_id=version_id)

    def restore_dashboard(self, dashboard_id: int = None, dashboard_uid: str = None, version_id: int = None):
        api_path = self.api_path(dashboard_id=dashboard_id, dashboard_uid=dashboard_uid)
        restore_dashboard_path = f"{api_path}/restore"

        if version_id is None:
            raise LookupError("version_id is required")

        r = self.client.POST(restore_dashboard_path, json={"version": version_id})
        return r

    def restore_dashboard_by_id(self, dashboard_id: int = None, version_id: int = None):
        return self.restore_dashboard(dashboard_id=dashboard_id, version_id=version_id)

    def restore_dashboard_by_uid(self, dashboard_uid: str = None, version_id: int = None):
        return self.restore_dashboard(dashboard_uid=dashboard_uid, version_id=version_id)

    def calculate_diff(
        self,
        base_dashboard_id: int,
        base_version_id: int,
        new_dashboard_id: int,
        new_version_id: int,
        diff_type: str = "json",
    ):
        """
        Compares two dashboard versions by calculating the JSON diff of them.

        :param diff_type: the type of diff to return. Can be "json" or "basic".
        """
        calculate_diff_path = "/dashboards/calculate-diff"

        if diff_type not in ["json", "basic"]:
            raise LookupError("diff_type must be either 'json' or 'basic'")

        r = self.client.POST(
            calculate_diff_path,
            json={
                "base": {"dashboardId": base_dashboard_id, "version": base_version_id},
                "new": {"dashboardId": new_dashboard_id, "version": new_version_id},
                "diffType": diff_type,
            },
        )
        return r
