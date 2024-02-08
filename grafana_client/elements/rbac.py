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

    def get_rbac_datasources(self, datasource_uid):
        """
        Gets all existing permissions for the data source with the given uid

        The Rbac is only available in Grafana Enterprise.
        This API works only with grafana version > 10.2.3.

        :param datasource_uid:
        :return:
        """
        datasource_path = "/access-control/datasources/%s" % datasource_uid
        r = self.client.GET(datasource_path)
        return r

    def set_rbac_datasources_teams(self, datasource_uid, team_id, permission):
        """
        Sets team permission for the data source with the given uid.

        the values allowed for the permission argument are :
        Query, Edit, or Admin.
        To remove a permission, set the permission argument to an empty string.
        The Rbac is only available in Grafana Enterprise.
        This API works only with grafana version > 10.2.3.

        :param datasource_uid:
        :param team_id:
        :param permission:
        :return:
        """
        datasource_path = "/access-control/datasources/%s/teams/%s" % (datasource_uid, team_id)
        r = self.client.POST(datasource_path, json={"permission": permission})
        return r

    def set_rbac_datasources_builtin_roles(self, datasource_uid, builtin_role, permission):
        """
        Sets permission for the data source with the given uid to all users who
        have the specified basic role.

        the values allowed for the builtin_role argument are :
        Admin, Editor or Viewer
        the values allowed for the permission argument are :
        Query, Edit, or Admin.
        To remove a permission, set the permission argument to an empty string.
        The Rbac is only available in Grafana Enterprise.
        This API works only with grafana version > 10.2.3.

        :param datasource_uid:
        :param builtin_role:
        :param permission:
        :return:
        """
        datasource_path = "/access-control/datasources/%s/builtInRoles/%s" % (datasource_uid, builtin_role)
        r = self.client.POST(datasource_path, json={"permission": permission})
        return r
