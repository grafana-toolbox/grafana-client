from .base import Base


class Dashboard(Base):
    def __init__(self, api):
        super(Dashboard, self).__init__(api)
        self.api = api

    def get_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        get_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.api.GET(get_dashboard_path)
        return r

    def update_dashboard(self, dashboard):
        """

        :param dashboard:
        :return:
        """
        put_dashboard_path = "/dashboards/db"
        r = self.api.POST(put_dashboard_path, json=dashboard)
        return r

    def delete_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        delete_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.api.DELETE(delete_dashboard_path)
        return r

    def get_home_dashboard(self):
        """

        :return:
        """
        get_home_dashboard_path = "/dashboards/home"
        r = self.api.GET(get_home_dashboard_path)
        return r

    def get_dashboards_tags(self):
        """

        :return:
        """
        get_dashboards_tags_path = "/dashboards/tags"
        r = self.api.GET(get_dashboards_tags_path)
        return r

    def get_dashboard_permissions(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        get_dashboard_permissions_path = "/dashboards/id/%s/permissions" % dashboard_id
        r = self.api.GET(get_dashboard_permissions_path)
        return r

    def update_dashboard_permissions(self, dashboard_id, items):
        """

        :param dashboard_id:
        :param items:
        :return:
        """
        update_dashboard_permissions_path = (
            "/dashboards/id/%s/permissions" % dashboard_id
        )
        r = self.api.POST(update_dashboard_permissions_path, json=items)
        return r
