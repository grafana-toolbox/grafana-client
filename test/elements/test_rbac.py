import unittest

import requests_mock

from grafana_client import GrafanaApi


class RbacTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_rbac_roles_all(self, m):
        m.get(
            "http://localhost/api/access-control/roles",
            json=[
                {
                    "version": 5,
                    "uid": "vi9mlLjGz",
                    "name": "fixed:datasources.permissions:writer",
                    "description": "Create, read or delete data source permissions.",
                    "global": True,
                    "updated": "2021-05-13T22:41:49+02:00",
                    "created": "2021-05-13T16:24:26+02:00",
                }
            ],
        )
        roles = self.grafana.rbac.get_rbac_roles_all()
        self.assertEqual(roles[0]["name"], "fixed:datasources.permissions:writer")
        self.assertEqual(len(roles), 1)

    @requests_mock.Mocker()
    def test_add_rbac_role_teams(self, m):
        m.post(
            "http://localhost/api/access-control/teams/1/roles",
            json={"message": "Role added to the team."},
        )
        history = m.request_history

        r = self.grafana.rbac.add_rbac_role_team("1", "XvHQJq57z")
        self.assertEqual(history[0].json()["roleUid"], "XvHQJq57z")
        self.assertEqual(r["message"], "Role added to the team.")

    @requests_mock.Mocker()
    def test_add_rbac_roles_teams(self, m):
        m.put(
            "http://localhost/api/access-control/teams/1/roles",
            json={"message": "Team roles have been updated."},
        )
        history = m.request_history

        roleUids = ["ZiHQJq5nk", "GzNQ1357k"]
        r = self.grafana.rbac.add_rbac_roles_team("1", roleUids)
        self.assertEqual(history[0].json()["roleUids"], roleUids)
        self.assertEqual(r["message"], "Team roles have been updated.")

    @requests_mock.Mocker()
    def test_remove_rbac_role_team(self, m):
        m.delete(
            "http://localhost/api/access-control/teams/1/roles/AFUXBHKnk",
            json={"message": "Role removed from team."},
        )
        r = self.grafana.rbac.remove_rbac_role_team("1", "AFUXBHKnk")
        self.assertEqual(r["message"], "Role removed from team.")
