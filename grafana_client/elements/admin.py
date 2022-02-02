from .base import Base


class Admin(Base):
    def __init__(self, client):
        super(Admin, self).__init__(client)
        self.client = client

    def settings(self):
        """

        :return:
        """
        path = "/admin/settings"
        r = self.client.GET(path)
        return r

    def stats(self):
        """

        :return:
        """
        path = "/admin/stats"
        r = self.client.GET(path)
        return r

    def create_user(self, user):
        """

        :param user:
        :return:
        """
        create_user_path = "/admin/users"
        r = self.client.POST(create_user_path, json=user)
        return r

    def change_user_password(self, user_id, password):
        """

        :param user_id:
        :param password:
        :return:
        """
        change_user_password_path = "/admin/users/%s/password" % user_id
        r = self.client.PUT(change_user_password_path, json={"password": password})
        return r

    def change_user_permissions(self, user_id, is_grafana_admin):
        """

        :param user_id:
        :param is_grafana_admin:
        :return:
        """
        change_user_permissions = "/admin/users/%s/permissions" % user_id
        r = self.client.PUT(change_user_permissions, json={"isGrafanaAdmin": is_grafana_admin})
        return r

    def delete_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        delete_user_path = "/admin/users/%s" % user_id
        r = self.client.DELETE(delete_user_path)
        return r

    def pause_all_alerts(self, pause):
        """

        :param pause:
        :return:
        """
        change_user_permissions = "/admin/pause-all-alerts"
        r = self.client.POST(change_user_permissions, json={"paused": pause})
        return r
