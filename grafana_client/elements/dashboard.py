from .base import Base


class Dashboard(Base):
    def __init__(self, client):
        super(Dashboard, self).__init__(client)
        self.client = client

    def get_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        get_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.client.GET(get_dashboard_path)
        return r

    def get_dashboard_by_name(self, dashboard_name):
        """

        :param dashboard_name:
        :return:
        """
        get_dashboard_path = "/dashboards/db/%s" % dashboard_name
        r = self.client.GET(get_dashboard_path)
        return r

    def update_dashboard(self, dashboard):
        """

        :param dashboard:
        :return:
        """

        # When the "folderId" is not available within the dashboard payload,
        # populate it from the nested "meta" object, if given.
        if "folderId" not in dashboard:
            if "meta" in dashboard and "folderId" in dashboard["meta"]:
                dashboard = dashboard.copy()
                dashboard["folderId"] = dashboard["meta"]["folderId"]

        put_dashboard_path = "/dashboards/db"
        r = self.client.POST(put_dashboard_path, json=dashboard)
        return r

    def delete_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        delete_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.client.DELETE(delete_dashboard_path)
        return r

    def get_home_dashboard(self):
        """

        :return:
        """
        get_home_dashboard_path = "/dashboards/home"
        r = self.client.GET(get_home_dashboard_path)
        return r

    def get_dashboards_tags(self):
        """

        :return:
        """
        get_dashboards_tags_path = "/dashboards/tags"
        r = self.client.GET(get_dashboards_tags_path)
        return r

    def get_dashboard_permissions(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        get_dashboard_permissions_path = "/dashboards/id/%s/permissions" % dashboard_id
        r = self.client.GET(get_dashboard_permissions_path)
        return r

    def update_dashboard_permissions(self, dashboard_id, items):
        """

        :param dashboard_id:
        :param items:
        :return:
        """
        update_dashboard_permissions_path = "/dashboards/id/%s/permissions" % dashboard_id
        r = self.client.POST(update_dashboard_permissions_path, json=items)
        return r
