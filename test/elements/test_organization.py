import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError, GrafanaClientError, GrafanaServerError, GrafanaUnauthorizedError
from grafana_client.model import PersonalPreferences

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class OrganizationTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api: GrafanaApi,
        user_with_organization,  # noqa: ARG002
        organization_id: int,
        user_id: int,
        dashboard_uid: str,
    ):

        self.grafana = grafana_api

        if Version(self.grafana.version) < Version("8"):
            pytest.skip("Unauthorized with vanilla Grafana 7")

        self.dashboard_uid = dashboard_uid
        self.organization_id = organization_id
        self.user_id = user_id
        self.angel_user = self.grafana.admin.create_user(
            {
                "login": "angel",
                "password": "secret",
                "OrgId": 1,
            }
        )

    def test_delete_user_by_id(self):
        annotation = self.grafana.organizations.organization_user_delete(organization_id=1, user_id=self.user_id)
        self.assertEqual("User removed from organization", annotation["message"])

    def test_preferences_update_get(self):
        response = self.grafana.organization.update_preferences(
            PersonalPreferences(theme="", homeDashboardUID=self.dashboard_uid, timezone="utc")
        )
        self.assertEqual(response["message"], "Preferences updated")

        result = self.grafana.organization.get_preferences()
        self.assertEqual("utc", result["timezone"])
        if Version(self.grafana.version) < Version("9"):
            self.assertEqual(0, result["homeDashboardId"])
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(self.dashboard_uid, result["homeDashboardUID"])

    def test_preferences_patch(self):
        response = self.grafana.organization.patch_preferences(PersonalPreferences(timezone="browser"))
        self.assertEqual("Preferences updated", response["message"])

    def test_organization_user_update_success(self):
        response = self.grafana.organizations.organization_user_update(
            organization_id=self.organization_id, user_id=self.user_id, user_role="Admin"
        )
        self.assertEqual("Organization user updated", response["message"])

    def test_organization_user_update_unknown_org(self):
        grafana_10_123 = Version("10") <= Version(self.grafana.version) < Version("10.4")

        def probe():
            self.grafana.organizations.organization_user_update(
                organization_id=9999, user_id=self.user_id, user_role="Admin"
            )

        if not grafana_10_123:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("Failed update org user", context.exception.message)
        else:
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(403, context.exception.status_code, "Wrong status code")
            self.assertIn("Permissions needed: org.users:write", context.exception.message)

    def test_organization_user_update_invalid_org(self):
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.organizations.organization_user_update(
                organization_id=-9999, user_id=self.user_id, user_role="Admin"
            )
        self.assertEqual(500, context.exception.status_code, "Wrong status code")
        self.assertIn("Failed update org user", context.exception.message)

    def test_organization_user_update_unknown_user(self):
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.organizations.organization_user_update(
                organization_id=self.organization_id, user_id=9999, user_role="Admin"
            )
        self.assertEqual(500, context.exception.status_code, "Wrong status code")
        self.assertIn("Failed update org user", context.exception.message)

    def test_organization_user_update_invalid_user(self):
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.organizations.organization_user_update(
                organization_id=self.organization_id, user_id=-9999, user_role="Admin"
            )
        self.assertEqual(500, context.exception.status_code, "Wrong status code")
        self.assertIn("Failed update org user", context.exception.message)

    def test_organization_user_add(self):
        response = self.grafana.organizations.organization_user_add(
            organization_id=self.organization_id, user={"loginOrEmail": "angel", "role": "Viewer"}
        )
        self.assertEqual("User added to organization", response["message"])

    def test_organization_user_list(self):
        users = self.grafana.organizations.organization_user_list(organization_id=1)
        self.assertEqual(3, len(users))

    def test_list_organization(self):
        users = self.grafana.organizations.list_organization()
        self.assertEqual(2, len(users))

    def test_get_current_organization(self):
        orgs = self.grafana.organization.get_current_organization()
        self.assertEqual("Main Org.", orgs["name"])

    def test_update_current_organization(self):
        response = self.grafana.organization.update_current_organization(organization={"name": "Main Org."})
        self.assertEqual("Organization updated", response["message"])

    def test_delete_current_organization(self):
        with self.assertRaises(GrafanaBadInputError) as context:
            self.grafana.organizations.delete_organization(organization_id=1)
        self.assertEqual(400, context.exception.status_code, "Wrong status code")
        if Version(self.grafana.version) >= Version("12"):
            self.assertIn("Cannot delete your active organization", context.exception.message)
        else:
            self.assertIn("Can not delete org for current user", context.exception.message)

    def test_update_organization_success(self):
        response = self.grafana.organizations.update_organization(
            organization_id=1, organization={"name": "Other Org 99."}
        )
        self.assertEqual("Organization updated", response["message"])

    def test_update_organization_unknown(self):
        grafana_10_123 = Version("10") <= Version(self.grafana.version) < Version("10.4")

        def probe():
            self.grafana.organizations.update_organization(organization_id=9999, organization={"name": "Other Org 99."})

        if not grafana_10_123:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("Failed to update organization", context.exception.message)
        else:
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(403, context.exception.status_code, "Wrong status code")
            self.assertIn("Permissions needed: orgs:write", context.exception.message)

    def test_delete_organization_success(self):
        response = self.grafana.organizations.delete_organization(organization_id=self.organization_id)
        self.assertEqual("Organization deleted", response["message"])

    def test_delete_organization_unknown(self):
        grafana_10_123 = Version("10") <= Version(self.grafana.version) < Version("10.4")
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.organizations.delete_organization(organization_id=9999)
        if not grafana_10_123:
            self.assertEqual(404, context.exception.status_code, "Wrong status code")
            self.assertIn("Failed to delete organization. ID not found", context.exception.message)
        else:
            self.assertEqual(403, context.exception.status_code, "Wrong status code")
            self.assertIn("You'll need additional permissions to perform this action", context.exception.message)

    def test_delete_organization_invalid(self):
        grafana_12_3 = Version("12.3") <= Version(self.grafana.version) < Version("12.4")
        if grafana_12_3:
            with self.assertRaises(GrafanaServerError) as context:
                self.grafana.organizations.delete_organization(organization_id=-9999)
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("Failed to delete organization", context.exception.message)
        else:
            with self.assertRaises(GrafanaClientError) as context:
                self.grafana.organizations.delete_organization(organization_id=-9999)
            self.assertEqual(404, context.exception.status_code, "Wrong status code")
            self.assertIn("Failed to delete organization. ID not found", context.exception.message)

    def test_create_organization_success(self):
        response = self.grafana.organization.create_organization(organization="New Org.")
        self.assertEqual("Organization created", response["message"])

    def test_create_organization_duplicate_name(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.organization.create_organization(organization="Main Org.")
        self.assertEqual(409, context.exception.status_code, "Wrong status code")
        self.assertIn("Organization name taken", context.exception.message)

    def test_delete_user_current_organization_success(self):
        response = self.grafana.organization.delete_user_current_organization(user_id=self.user_id)
        self.assertEqual("User removed from organization", response["message"])

    @pytest.mark.skip(reason="Please investigate!")
    def test_delete_user_current_organization_not_member(self):
        response = self.grafana.organization.delete_user_current_organization(user_id=self.user_id)
        # TODO: Review -- shouldn't this be `User removed from organization`?
        #       https://grafana.com/docs/grafana/v12.0/developers/http_api/org/#delete-user-in-current-organization
        self.assertEqual("User deleted", response["message"])

    def test_delete_user_current_organization_last_admin_forbidden(self):
        with self.assertRaises(GrafanaBadInputError) as context:
            self.grafana.organization.delete_user_current_organization(user_id=1)
        self.assertIn("Cannot remove last organization admin", context.exception.message)

    def test_add_user_current_organization_success(self):
        self.grafana.admin.create_user(
            {
                "login": "new-user",
                "password": "secret",
                "OrgId": self.organization_id,
            }
        )
        response = self.grafana.organization.add_user_current_organization(
            {"role": "Admin", "loginOrEmail": "new-user"}
        )
        self.assertEqual("User added to organization", response["message"])

    def test_add_user_current_organization_already_member(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.organization.add_user_current_organization({"role": "Admin", "loginOrEmail": "admin"})
        self.assertEqual(409, context.exception.status_code, "Wrong status code")
        self.assertIn("User is already member of this organization", context.exception.message)

    def test_add_user_current_organization_user_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.organization.add_user_current_organization({"role": "Admin", "loginOrEmail": "unknown"})
        self.assertEqual(404, context.exception.status_code, "Wrong status code")
        self.assertIn("User not found", context.exception.message)

    def test_update_user_current_organization_success(self):
        user = self.grafana.admin.create_user(
            {
                "login": "new-user",
                "password": "secret",
                "OrgId": 1,
            }
        )
        response = self.grafana.organization.update_user_current_organization(
            user_id=user["id"],
            user={"role": "Viewer"},
        )
        self.assertEqual("Organization user updated", response["message"])

    def test_update_user_current_organization_user_unknown(self):
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.organization.update_user_current_organization(
                user_id=9999,
                user={"role": "Viewer"},
            )
        self.assertEqual(500, context.exception.status_code, "Wrong status code")
        self.assertIn("Failed update org user", context.exception.message)

    def test_get_current_organization_users(self):
        org = self.grafana.organization.get_current_organization_users()
        self.assertEqual(3, len(org), "Wrong number of users")

    def test_find_organization_success(self):
        org = self.grafana.organization.find_organization(org_name="Testdrive Org.")
        self.assertEqual(org["id"], self.organization_id)

    def test_find_organization_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.organization.find_organization(org_name="unknown")
        self.assertEqual(404, context.exception.status_code, "Wrong status code")
        self.assertIn("Organization not found", context.exception.message)


def test_switch_organization_success(grafana_api: GrafanaApi, reset_organization_switch, organization_id: str):  # noqa: ARG001
    response = grafana_api.organizations.switch_organization(organization_id=organization_id)
    assert response["message"] == "Active organization changed"
    org = grafana_api.organization.get_current_organization()
    assert org["name"] == "Testdrive Org."


def test_switch_organization_unknown(grafana_api: GrafanaApi):
    with pytest.raises(GrafanaUnauthorizedError) as context:
        grafana_api.organizations.switch_organization(organization_id=9999)
    assert context.value.status_code == 401, "Wrong status code"
    assert context.value.message == "Unauthorized"
