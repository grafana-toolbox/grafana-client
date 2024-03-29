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
        return self.client.GET(path)

    def stats(self):
        """

        :return:
        """
        path = "/admin/stats"
        return self.client.GET(path)

    def create_user(self, user):
        """

        :param user:
        :return:
        """
        create_user_path = "/admin/users"
        return self.client.POST(create_user_path, json=user)

    def change_user_password(self, user_id, password):
        """

        :param user_id:
        :param password:
        :return:
        """
        change_user_password_path = "/admin/users/%s/password" % user_id
        return self.client.PUT(change_user_password_path, json={"password": password})

    def change_user_permissions(self, user_id, is_grafana_admin):
        """

        :param user_id:
        :param is_grafana_admin:
        :return:
        """
        change_user_permissions = "/admin/users/%s/permissions" % user_id
        return self.client.PUT(change_user_permissions, json={"isGrafanaAdmin": is_grafana_admin})

    def delete_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        delete_user_path = "/admin/users/%s" % user_id
        return self.client.DELETE(delete_user_path)

    def pause_all_alerts(self, pause):
        """

        :param pause:
        :return:
        """
        change_user_permissions = "/admin/pause-all-alerts"
        return self.client.POST(change_user_permissions, json={"paused": pause})

    def set_user_enabled(self, user_id, enabled: bool):
        """

        :param user_id:
        :param enabled:
        :return:
        """
        action = "enable" if enabled else "disable"
        set_user_enabled = "/admin/users/%s/%s" % (user_id, action)
        return self.client.POST(set_user_enabled)
