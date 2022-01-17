from ensurepip import version
import json
from .base import Base

class Dashboard_version(Base):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
    
    def get_dashboard_versions(self, dashboard_id, limit, start):
        """

        :param dashboard_id:
        :param limit:
        :param start:
        :return:
        """
        get_dashboard_versions_path = f"/api/dashboards/id/{dashboard_id}/versions"
        get_dashboard_versions_path += f"?limit={limit}"
        get_dashboard_versions_path += f"?start={start}"

        r = self.api.GET(get_dashboard_versions_path)
        return r
    
    def get_dashboard_version(self, dashboard_id, versionid):
        """

        :param dashboard_id:
        :param versionid:
        :return:
        """
        get_dashboard_version_path = f"/api/dashboards/id/{dashboard_id}/versions/{versionid}"

        r = self.api.GET(get_dashboard_version_path)
        return r

    def restore_dashboard(self, dashboard_id, versionid):
        """

        :param dashboard_id:
        :param versionid:
        :return:
        """
        restore_dashboard_path = f"/api/dashboards/id/{dashboard_id}/restore"

        r = self.api.POST(
            restore_dashboard_path,
            json={
                "version": f"{versionid}"
                }
            )
        return r

    def calculate_diff(self, basedashboard_id, baseversionid, newdashboard_id, newversionid, difftype):
        """

        :param dashboard_id:
        :param versionid:
        :return:
        """
        calculate_diff_path = f"/api/dashboards/calculate-diff"

        r = self.api.POST(
            calculate_diff_path,
            json={
                "base": {
                    "dashboardId": f"{basedashboard_id}",
                    "version": f"{baseversionid}"
                },
                "new": {
                    "dashboardId": f"{newdashboard_id}",
                    "version": f"{newversionid}"
                },
                "diffType": f"{difftype}"
                }
        )
        return r