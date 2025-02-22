import warnings

from verlib2 import Version

from ..base import Base

VERSION_8 = Version("8")


class Dashboard(Base):
    def __init__(self, client, api):
        super(Dashboard, self).__init__(client)
        self.client = client
        self.api = api

    async def get_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        get_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        return await self.client.GET(get_dashboard_path)

    async def get_dashboard_by_name(self, dashboard_name):
        """

        :param dashboard_name:
        :return:
        """
        if await self.api.version and Version(await self.api.version) >= VERSION_8:
            raise DeprecationWarning("Grafana 8 and higher does not support getting dashboards by slug")
        get_dashboard_path = "/dashboards/db/%s" % dashboard_name
        return await self.client.GET(get_dashboard_path)

    async def update_dashboard(self, dashboard):
        """

        :param dashboard:
        :return:
        """

        # When `folderId` or `folderUid` are not available within the dashboard payload,
        # populate them from the nested `meta` object, when given.
        for attribute in ["folderId", "folderUid"]:
            if attribute not in dashboard:
                if "meta" in dashboard and attribute in dashboard["meta"]:
                    dashboard = dashboard.copy()
                    dashboard[attribute] = dashboard["meta"][attribute]

        put_dashboard_path = "/dashboards/db"
        return await self.client.POST(put_dashboard_path, json=dashboard)

    async def delete_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        delete_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        return await self.client.DELETE(delete_dashboard_path)

    async def get_home_dashboard(self):
        """

        :return:
        """
        get_home_dashboard_path = "/dashboards/home"
        return await self.client.GET(get_home_dashboard_path)

    async def get_dashboards_tags(self):
        """

        :return:
        """
        get_dashboards_tags_path = "/dashboards/tags"
        return await self.client.GET(get_dashboards_tags_path)

    async def get_dashboard_permissions(self, dashboard_id):
        warnings.warn(
            "get_dashboard_permissions is deprecated, use corresponding _by_id or _by_uid methods",
            DeprecationWarning,
        )
        return self.get_permissions_by_id(dashboard_id)

    async def update_dashboard_permissions(self, dashboard_id, items):
        warnings.warn(
            "update_dashboard_permissions is deprecated, use corresponding _by_id or _by_uid methods",
            DeprecationWarning,
        )
        return self.update_permissions_by_id(dashboard_id, items)

    async def get_permissions_by_id(self, dashboard_id):
        return self.get_permissions_generic(dashboard_id, idtype="id")

    async def update_permissions_by_id(self, dashboard_id, items):
        return self.update_permissions_generic(dashboard_id, items, idtype="id")

    async def get_permissions_by_uid(self, dashboard_id):
        return self.get_permissions_generic(dashboard_id)

    async def update_permissions_by_uid(self, dashboard_id, items):
        return self.update_permissions_generic(dashboard_id, items)

    async def get_permissions_generic(self, identifier, idtype="uid"):
        permissions_path = f"/dashboards/{idtype}/{identifier}/permissions"
        return await self.client.GET(permissions_path)

    async def update_permissions_generic(self, identifier, items, idtype="uid"):
        permissions_path = f"/dashboards/{idtype}/{identifier}/permissions"
        return await self.client.POST(permissions_path, json=items)
