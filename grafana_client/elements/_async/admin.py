from ..base import Base


class Admin(Base):
    def __init__(self, client):
        super(Admin, self).__init__(client)
        self.client = client

    async def settings(self):
        """

        :return:
        """
        path = "/admin/settings"
        r = await self.client.GET(path)
        return r

    async def stats(self):
        """

        :return:
        """
        path = "/admin/stats"
        r = await self.client.GET(path)
        return r

    async def create_user(self, user):
        """

        :param user:
        :return:
        """
        create_user_path = "/admin/users"
        r = await self.client.POST(create_user_path, json=user)
        return r

    async def change_user_password(self, user_id, password):
        """

        :param user_id:
        :param password:
        :return:
        """
        change_user_password_path = "/admin/users/%s/password" % user_id
        r = await self.client.PUT(change_user_password_path, json={"password": password})
        return r

    async def change_user_permissions(self, user_id, is_grafana_admin):
        """

        :param user_id:
        :param is_grafana_admin:
        :return:
        """
        change_user_permissions = "/admin/users/%s/permissions" % user_id
        r = await self.client.PUT(change_user_permissions, json={"isGrafanaAdmin": is_grafana_admin})
        return r

    async def delete_user(self, user_id):
        """

        :param user_id:
        :return:
        """
        delete_user_path = "/admin/users/%s" % user_id
        r = await self.client.DELETE(delete_user_path)
        return r

    async def pause_all_alerts(self, pause):
        """

        :param pause:
        :return:
        """
        change_user_permissions = "/admin/pause-all-alerts"
        r = await self.client.POST(change_user_permissions, json={"paused": pause})
        return r

    async def set_user_enabled(self, user_id, enabled: bool):
        """

        :param user_id:
        :param enabled:
        :return:
        """
        action = "enable" if enabled else "disable"
        set_user_enabled = "/admin/users/%s/%s" % (user_id, action)
        r = await self.client.POST(set_user_enabled)
        return r
