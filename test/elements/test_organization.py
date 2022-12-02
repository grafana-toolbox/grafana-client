import unittest

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.model import PersonalPreferences


class OrganizationTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_delete_snapshot_by_key(self, m):
        m.delete("http://localhost/api/orgs/1/users/2", json={"message": "User removed from organization"})
        annotation = self.grafana.organizations.organization_user_delete(organization_id=1, user_id=2)
        self.assertEqual(annotation["message"], "User removed from organization")

    @requests_mock.Mocker()
    def test_organization_preference_get(self, m):
        m.get("http://localhost/api/org/preferences", json={"theme": "", "homeDashboardId": 0, "timezone": ""})

        result = self.grafana.organizations.organization_preference_get()
        self.assertEqual(result["homeDashboardId"], 0)

    @requests_mock.Mocker()
    def test_organization_preference_update(self, m):
        m.put("http://localhost/api/org/preferences", json={"message": "Preferences updated"})
        preference = self.grafana.organizations.organization_preference_update(
            theme="", home_dashboard_id=0, timezone="utc"
        )
        self.assertEqual(preference["message"], "Preferences updated")

    @requests_mock.Mocker()
    def test_get_preferences(self, m):
        m.get("http://localhost/api/org/preferences", json={"theme": "", "homeDashboardId": 0, "timezone": ""})

        result = self.grafana.organization.get_preferences()
        self.assertEqual(result["homeDashboardId"], 0)

    @requests_mock.Mocker()
    def test_update_preferences(self, m):
        m.put("http://localhost/api/org/preferences", json={"message": "Preferences updated"})
        preference = self.grafana.organization.update_preferences(
            PersonalPreferences(theme="", homeDashboardId=999, timezone="utc")
        )
        self.assertEqual(preference["message"], "Preferences updated")

    @requests_mock.Mocker()
    def test_patch_preferences(self, m):
        m.patch("http://localhost/api/org/preferences", json={"message": "Preferences updated"})
        preference = self.grafana.organization.patch_preferences(PersonalPreferences(homeDashboardUID="zgjG8dKVz"))
        self.assertEqual(preference["message"], "Preferences updated")

    @requests_mock.Mocker()
    def test_organization_user_update(self, m):
        m.patch("http://localhost/api/orgs/1/users/2", json={"message": "Organization user updated"})
        preference = self.grafana.organizations.organization_user_update(
            organization_id=1, user_id=2, user_role="Admin"
        )
        self.assertEqual(preference["message"], "Organization user updated")

    @requests_mock.Mocker()
    def test_organization_user_add(self, m):
        m.post("http://localhost/api/orgs/1/users", json={"message": "User added to organization"})
        preference = self.grafana.organizations.organization_user_add(
            organization_id=1, user={"loginOrEmail": "user", "role": "Viewer"}
        )
        self.assertEqual(preference["message"], "User added to organization")

    @requests_mock.Mocker()
    def test_organization_user_list(self, m):
        m.get(
            "http://localhost/api/orgs/1/users",
            json=[{"orgId": 1, "userId": 1, "email": "admin@mygraf.com", "login": "admin", "role": "Admin"}],
        )
        users = self.grafana.organizations.organization_user_list(organization_id=1)
        self.assertEqual(len(users), 1)

    @requests_mock.Mocker()
    def test_list_organization(self, m):
        m.get(
            "http://localhost/api/orgs",
            json=[{"orgId": 1, "userId": 1, "email": "admin@mygraf.com", "login": "admin", "role": "Admin"}],
        )
        users = self.grafana.organizations.list_organization()
        self.assertEqual(len(users), 1)

    @requests_mock.Mocker()
    def test_get_current_organization(self, m):
        m.get("http://localhost/api/org", json={"id": 1, "name": "Main Org."})
        orgs = self.grafana.organization.get_current_organization()
        self.assertEqual(orgs["name"], "Main Org.")

    @requests_mock.Mocker()
    def test_update_current_organization(self, m):
        m.put("http://localhost/api/org", json={"message": "Organization updated"})
        org = self.grafana.organization.update_current_organization(organization={"name": "Main Org."})
        self.assertEqual(org["message"], "Organization updated")

    @requests_mock.Mocker()
    def test_update_organization(self, m):
        m.put("http://localhost/api/orgs/1", json={"message": "Organization updated"})
        preference = self.grafana.organizations.update_organization(
            organization_id=1, organization={"name": "Main Org 2."}
        )
        self.assertEqual(preference["message"], "Organization updated")

    @requests_mock.Mocker()
    def test_delete_organization(self, m):
        m.delete("http://localhost/api/orgs/1", json={"message": "Organization deleted"})
        preference = self.grafana.organizations.delete_organization(organization_id=1)
        self.assertEqual(preference["message"], "Organization deleted")

    @requests_mock.Mocker()
    def test_create_organization(self, m):
        m.post("http://localhost/api/orgs", json={"orgId": "1", "message": "Organization created"})
        preference = self.grafana.organization.create_organization(organization={"name": "New Org."})
        self.assertEqual(preference["message"], "Organization created")

    @requests_mock.Mocker()
    def test_delete_user_current_organization(self, m):
        m.delete("http://localhost/api/org/users/1", json={"message": "User removed from organization"})
        preference = self.grafana.organization.delete_user_current_organization(user_id=1)
        self.assertEqual(preference["message"], "User removed from organization")

    @requests_mock.Mocker()
    def test_add_user_current_organization(self, m):
        m.post("http://localhost/api/org/users", json={"message": "User added to organization"})
        preference = self.grafana.organization.add_user_current_organization({"role": "Admin", "loginOrEmail": "admin"})
        self.assertEqual(preference["message"], "User added to organization")

    @requests_mock.Mocker()
    def test_update_user_current_organization(self, m):
        m.patch("http://localhost/api/org/users/1", json={"message": "Organization user updated"})
        preference = self.grafana.organization.update_user_current_organization(
            user_id=1,
            user={
                "role": "Viewer",
            },
        )
        self.assertEqual(preference["message"], "Organization user updated")

    @requests_mock.Mocker()
    def test_get_current_organization_users(self, m):
        m.get(
            "http://localhost/api/org/users",
            json=[{"orgId": 1, "userId": 1, "email": "admin@mygraf.com", "login": "admin", "role": "Admin"}],
        )
        org = self.grafana.organization.get_current_organization_users()
        self.assertEqual(len(org), 1)

    @requests_mock.Mocker()
    def test_find_organization(self, m):
        m.get(
            "http://localhost/api/orgs/name/Main",
            json={
                "id": 1,
                "name": "Main Org.",
                "address": {"address1": "", "address2": "", "city": "", "zipCode": "", "state": "", "country": ""},
            },
        )
        org = self.grafana.organization.find_organization(org_name="Main")
        self.assertEqual(org["id"], 1)

    @requests_mock.Mocker()
    def test_switch_organization(self, m):
        m.post("http://localhost/api/user/using/2", json={"message": "Active organization changed"})
        preference = self.grafana.organizations.switch_organization(organization_id=2)
        self.assertEqual(preference["message"], "Active organization changed")
