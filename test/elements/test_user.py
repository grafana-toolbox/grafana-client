import sys
import unittest
from unittest import mock

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError, GrafanaClientError, GrafanaServerError, GrafanaUnauthorizedError
from grafana_client.model import PersonalPreferences

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class UsersTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api: GrafanaApi,
        reset_stars,  # noqa: ARG002
        user_with_organization,  # noqa: ARG002
        user_id: int,
    ):
        self.grafana = grafana_api
        self.user_id = user_id

    def test_update_user_success(self):
        response = self.grafana.users.update_user(self.user_id, {"login": "foo"})
        self.assertEqual("User updated", response["message"])

    def test_update_user_empty(self):
        with self.assertRaises(GrafanaBadInputError) as context:
            self.grafana.users.update_user(self.user_id, {})
        self.assertEqual(400, context.exception.status_code)
        if self.grafana.get_version() >= Version("10"):
            self.assertIn("Need to specify either username or email", context.exception.message)
        else:
            self.assertIn("Validation error, need to specify either username or email", context.exception.message)

    def test_update_user_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.users.update_user("unknown", {})
        if self.grafana.get_version() >= Version("11"):
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("User not found", context.exception.message)
        else:
            self.assertEqual(400, context.exception.status_code)
            if self.grafana.get_version() >= Version("8"):
                self.assertIn("id is invalid", context.exception.message)
            else:
                self.assertIn("Validation error, need to specify either username or email", context.exception.message)

    def test_get_user_success(self):
        user = self.grafana.users.get_user(self.user_id)
        self.assertEqual("testdrive", user["login"])
        self.assertEqual("testdrive", user["email"])
        self.assertEqual("", user["name"])

    def test_get_user_unknown(self):
        grafana_7_lower = self.grafana.get_version() < Version("8")
        grafana_11_greater = self.grafana.get_version() >= Version("11")
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.users.get_user("unknown")
        if grafana_7_lower or grafana_11_greater:
            self.assertEqual(404, context.exception.status_code)
            self.assertRegex(context.exception.message, "[Uu]ser not found")
        else:
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("id is invalid", context.exception.message)

    def test_find_user_success(self):
        user = self.grafana.users.find_user("testdrive")
        self.assertEqual("testdrive", user["login"])

    def test_find_user_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.users.find_user("unknown")
        self.assertEqual(404, context.exception.status_code)
        self.assertRegex(context.exception.message, "[Uu]ser not found")

    def test_search_users_success(self):
        users = self.grafana.users.search_users("testdrive")
        self.assertEqual(1, len(users), "Wrong number of users")

    def test_search_users_unknown(self):
        users = self.grafana.users.search_users("unknown")
        self.assertEqual(0, len(users), "Wrong number of users")

    def test_search_users_page2(self):
        users = self.grafana.users.search_users("testdrive", page=2)
        self.assertEqual(0, len(users), "Wrong number of users")

    def test_search_users_perpage(self):
        users = self.grafana.users.search_users("testdrive", perpage=1)
        self.assertEqual(1, len(users), "Wrong number of users")

    def test_search_users_perpage_no_endless_loop(self):
        users = self.grafana.users.search_users("testdrive", perpage=5)
        self.assertEqual(1, len(users), "Wrong number of users")

    def test_get_user_organisations(self):
        users = self.grafana.users.get_user_organisations(self.user_id)
        self.assertEqual(2, len(users), "Wrong number of organisations")
        self.assertEqual(
            [
                {"name": "Main Org.", "orgId": mock.ANY, "role": "Viewer"},
                {"name": "Testdrive Org.", "orgId": mock.ANY, "role": "Viewer"},
            ],
            users,
        )


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class UserTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api: GrafanaApi,
        reset_stars,  # noqa: ARG002
        user_with_organization,  # noqa: ARG002
        user_id,
        organization_id,
        dashboard_id,
        dashboard_uid,
    ):
        self.grafana = grafana_api
        self.user_id = user_id
        self.organization_id = organization_id
        self.dashboard_id = dashboard_id
        self.dashboard_uid = dashboard_uid

    def test_get_actual_user_success(self):
        user = self.grafana.user.get_actual_user()
        self.assertEqual("admin", user["login"])

    @pytest.mark.skip("Changing the password would leave the test suite stranded (Unauthorized).")
    def test_change_password_success(self):
        response = self.grafana.user.change_actual_user_password("admin", "adminadmin")
        self.assertEqual("User password changed", response["message"])

    def test_change_password_invalid(self):
        def probe():
            self.grafana.user.change_actual_user_password("invalid", "new")

        if self.grafana.get_version() >= Version("11"):
            with self.assertRaises(GrafanaBadInputError) as context:
                probe()
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("Invalid old password", context.exception.message)
        else:
            with self.assertRaises(GrafanaUnauthorizedError) as context:
                probe()
            self.assertEqual(401, context.exception.status_code)
            self.assertIn("Unauthorized", context.exception.message)

    def test_change_password_too_short(self):
        grafana_10_4 = Version("10.4") <= self.grafana.get_version() < Version("11")

        def probe():
            self.grafana.user.change_actual_user_password("admin", "new")

        # TODO: Should that particular anomaly with Grafana 10.4 be reported?
        if grafana_10_4:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code)
            self.assertIn("Internal Server Error", context.exception.message)
        else:
            with self.assertRaises(GrafanaBadInputError) as context:
                probe()
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("New password is too short", context.exception.message)

    # @pytest.mark.skip("Currently fails (Unauthorized).")
    def test_switch_user_organisation_success(self):
        response = self.grafana.user.switch_user_organisation(self.user_id, self.organization_id)
        self.assertEqual("Active organization changed", response["message"])

    def test_switch_user_organisation_unknown_user(self):
        with self.assertRaises(GrafanaUnauthorizedError) as context:
            self.grafana.user.switch_user_organisation(9999, self.organization_id)
        self.assertEqual(401, context.exception.status_code)
        self.assertIn("Unauthorized", context.exception.message)

    def test_switch_user_organisation_unknown_org(self):
        if self.grafana.version == "nightly":
            pytest.skip(
                "Grafana Nightly: Skipping switching to unknown organisation. "
                "Reason: Read timed out. (read timeout=5.0)"
            )

        def probe():
            return self.grafana.user.switch_user_organisation(self.user_id, "acme")

        if self.grafana.get_version() >= Version("8"):
            with self.assertRaises(GrafanaBadInputError) as context:
                probe()
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("orgId is invalid", context.exception.message)
        else:
            with self.assertRaises(GrafanaUnauthorizedError) as context:
                probe()
            self.assertEqual(401, context.exception.status_code)
            self.assertIn("Unauthorized", context.exception.message)

    def test_switch_actual_user_organisation_success(self):
        response = self.grafana.user.switch_actual_user_organisation(self.organization_id)
        self.assertEqual("Active organization changed", response["message"])

    def test_switch_actual_user_organisation_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.user.switch_actual_user_organisation("unknown")
        if self.grafana.get_version() >= Version("8"):
            self.assertEqual(400, context.exception.status_code)
            self.assertIn("id is invalid", context.exception.message)
        else:
            self.assertEqual(401, context.exception.status_code)
            self.assertIn("Unauthorized", context.exception.message)

    def test_get_actual_user_organisations(self):
        result = self.grafana.user.get_actual_user_organisations()
        self.assertEqual(
            [
                {"name": "Main Org.", "orgId": 1, "role": "Admin"},
                {"name": "Testdrive Org.", "orgId": mock.ANY, "role": "Admin"},
            ],
            result,
        )

    def test_star_dashboard_by_uid(self):
        if self.grafana.get_version() < Version("9"):
            pytest.skip("Starring dashboards by uid only supported by Grafana 9 and higher.")
        response = self.grafana.user.star_dashboard(self.dashboard_uid)
        self.assertEqual("Dashboard starred!", response["message"])

    def test_unstar_dashboard_by_uid(self):
        if self.grafana.get_version() < Version("9"):
            pytest.skip("Starring dashboards by uid only supported by Grafana 9 and higher.")
        response = self.grafana.user.unstar_dashboard(self.dashboard_uid)
        self.assertEqual("Dashboard unstarred", response["message"])

    def test_star_dashboard_by_id(self):
        if self.grafana.get_version() >= Version("12"):
            pytest.skip("Starring dashboards by id only supported until Grafana 11.")
        response = self.grafana.user.star_dashboard(self.dashboard_id)
        self.assertEqual("Dashboard starred!", response["message"])

    def test_unstar_dashboard_by_id(self):
        if self.grafana.get_version() >= Version("12"):
            pytest.skip("Starring dashboards by id only supported until Grafana 11.")
        response = self.grafana.user.unstar_dashboard(self.dashboard_id)
        self.assertEqual("Dashboard unstarred", response["message"])

    def test_get_preferences(self):
        self.grafana.user.update_preferences({}, filter_none=False)
        prefs = self.grafana.user.get_preferences()
        prefs_keys = sorted(prefs.keys())
        if self.grafana.get_version() >= Version("9"):
            self.assertIn(prefs_keys, [[], ["homeDashboardUID"]])
        elif self.grafana.get_version() >= Version("8"):
            self.assertEqual(["homeDashboardId", "navbar", "theme", "timezone", "weekStart"], prefs_keys)
        else:
            self.assertEqual(["homeDashboardId", "theme", "timezone"], prefs_keys)

    def test_update_preferences_success(self):
        response = self.grafana.user.update_preferences(PersonalPreferences(theme="", timezone="utc"))
        self.assertEqual("Preferences updated", response["message"])

    def test_update_preferences_unknown_dashboard(self):
        def probe():
            return self.grafana.user.update_preferences(PersonalPreferences(homeDashboardId=9999))

        if self.grafana.get_version() >= Version("12"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("Dashboard not found", context.exception.message)
        else:
            response = probe()
            self.assertEqual("Preferences updated", response["message"])

    def test_patch_preferences_success(self):

        def probe():
            return self.grafana.user.patch_preferences(PersonalPreferences(homeDashboardUID=self.dashboard_uid))

        if self.grafana.get_version() >= Version("8"):
            response = probe()
            self.assertEqual("Preferences updated", response["message"])
        else:
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertRegex(context.exception.message, "Not found")

    def test_patch_preferences_unknown_dashboard(self):
        grafana_7_lower = self.grafana.get_version() < Version("8")
        grafana_9_higher = self.grafana.get_version() >= Version("9")

        def probe():
            return self.grafana.user.patch_preferences(PersonalPreferences(homeDashboardUID="unknown"))

        if grafana_7_lower or grafana_9_higher:
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertRegex(context.exception.message, "(Dashboard )?[Nn]ot found")

        # Grafana 8 accepts the patch, even when referenced dashboard does not exist.
        else:
            response = probe()
            self.assertEqual("Preferences updated", response["message"])
