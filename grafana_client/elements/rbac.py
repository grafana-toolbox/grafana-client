from .base import Base


class Rbac(Base):
    def __init__(self, client):
        super(Rbac, self).__init__(client)
        self.client = client

    def get_rbac_roles_all(self):
        """
        The Rbac is only available in Grafana Enterprise.

        :return:
        """
        roles_path = "/access-control/roles"
        r = self.client.GET(roles_path)
        return r

    def add_rbac_role_team(self, team_id, role_uid):
        """
        The Rbac is only available in Grafana Enterprise.

        :param team_id:
        :param role_uid:
        :return:
        """
        role_team_path = "/access-control/teams/%s/roles" % team_id
        r = self.client.POST(role_team_path, json={"roleUid": role_uid})
        return r

    def add_rbac_roles_team(self, team_id, role_uids):
        """
        The Rbac is only available in Grafana Enterprise.

        :param team_id:
        :param role_uids:
        :return:
        """
        role_team_path = "/access-control/teams/%s/roles" % team_id
        r = self.client.PUT(role_team_path, json={"roleUids": role_uids})
        return r

    def remove_rbac_role_team(self, team_id, role_uid):
        """
        The Rbac is only available in Grafana Enterprise.

        :param team_id:
        :param role_uid:
        :return:
        """
        role_team_path = "/access-control/teams/%s/roles/%s" % (team_id, role_uid)
        r = self.client.DELETE(role_team_path)
        return r
