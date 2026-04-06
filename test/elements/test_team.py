import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError, GrafanaServerError
from grafana_client.model import PersonalPreferences

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class TeamsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi, user_id: int):
        self.grafana = grafana_api
        self.user_id = user_id
        self.first_team = self.grafana.teams.add_team("my team")
        self.second_team = self.grafana.teams.add_team("SecondTeam")
        self.first_team_id = self.first_team["teamId"]
        self.second_team_id = self.second_team["teamId"]

    def test_search_teams_url_encodes_query(self):
        teams = self.grafana.teams.search_teams("my team")
        self.assertEqual(1, len(teams))
        self.assertEqual("my team", teams[0]["name"])

    def test_search_teams_loads_all_pages(self):
        teams = self.grafana.teams.search_teams("team", perpage=1)
        self.assertEqual(2, len(teams))
        self.assertEqual({"my team", "SecondTeam"}, {team["name"] for team in teams})

    def test_search_teams_only_loads_requested_page(self):
        teams = self.grafana.teams.search_teams("my team", page=2)
        self.assertEqual(0, len(teams))

    def test_search_teams_perpage(self):
        teams = self.grafana.teams.search_teams("team", perpage=5)
        self.assertEqual(2, len(teams))

    def test_get_team_by_name(self):
        teams = self.grafana.teams.get_team_by_name("my team")
        self.assertEqual("my team", teams[0]["name"])
        self.assertEqual(1, len(teams))

    def test_get_team_by_id_success(self):
        team = self.grafana.teams.get_team(self.second_team_id)
        self.assertEqual("SecondTeam", team["name"])

    def test_get_team_by_id_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.teams.get_team(9999)
        self.assertEqual(404, context.exception.status_code)
        self.assertIn("Team not found", context.exception.message)

    def test_add_team_success(self):
        team = {"name": "MySecondTestTeam", "email": "email@example.org"}
        response = self.grafana.teams.add_team(team)
        self.assertEqual("Team created", response["message"])

    def test_update_team_success(self):
        team = {"name": "MyThirdTestTeam", "email": "email@example.org"}
        response = self.grafana.teams.update_team(self.first_team_id, team)
        self.assertEqual("Team updated", response["message"])

    def test_update_team_unknown(self):
        def probe():
            self.grafana.teams.update_team(9999, {})

        if Version(self.grafana.version) >= Version("12"):
            with self.assertRaises(GrafanaClientError) as context:
                probe()
            self.assertEqual(404, context.exception.status_code)
            self.assertIn("Team not found", context.exception.message)
        else:
            with self.assertRaises(GrafanaServerError) as context:
                probe()
            self.assertEqual(500, context.exception.status_code)
            self.assertIn("Failed to update Team", context.exception.message)

    def test_delete_team_success(self):
        response = self.grafana.teams.delete_team(self.first_team_id)
        self.assertEqual("Team deleted", response["message"])

    def test_delete_team_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.teams.delete_team(9999)
        self.assertEqual(404, context.exception.status_code)
        self.assertRegex(context.exception.message, "(Team not found|Failed to delete Team. ID not found)")

    def test_get_team_members(self):
        members = self.grafana.teams.get_team_members(self.first_team_id)
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual("admin", members[0]["login"])
        else:
            self.assertEqual([], members)

    def test_add_team_member(self):
        response = self.grafana.teams.add_team_member(self.first_team_id, self.user_id)
        self.assertEqual("Member added to Team", response["message"])

    def test_remove_team_member(self):
        self.grafana.teams.add_team_member(self.first_team_id, self.user_id)
        response = self.grafana.teams.remove_team_member(self.first_team_id, self.user_id)
        self.assertEqual("Team Member removed", response["message"])

    def test_get_team_preferences(self):
        """
        Legacy method.
        """
        prefs = {"theme": "light", "homeDashboardId": 0, "timezone": "utc"}
        self.grafana.teams.update_team_preferences(self.first_team_id, prefs)
        prefs = self.grafana.teams.get_team_preferences(self.first_team_id)
        self.assertEqual("utc", prefs["timezone"])

    def test_update_team_preferences(self):
        """
        Legacy method, using a dictionary.
        """
        prefs = {"theme": "light", "homeDashboardId": 0, "timezone": "utc"}
        response = self.grafana.teams.update_team_preferences(self.first_team_id, prefs)
        self.assertEqual("Preferences updated", response["message"])

    def test_get_preferences(self):
        """
        Modern method.
        """
        prefs = self.grafana.teams.get_preferences(self.second_team_id)
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual({}, prefs)
        elif Version(self.grafana.version) >= Version("8"):
            self.assertEqual(["homeDashboardId", "navbar", "theme", "timezone", "weekStart"], sorted(prefs.keys()))
        else:
            self.assertEqual(["homeDashboardId", "theme", "timezone"], sorted(prefs.keys()))

    def test_update_preferences(self):
        """
        Modern method, using a `PersonalPreferences` instance.
        """
        prefs = PersonalPreferences(theme="light", homeDashboardId=0, timezone="utc")
        response = self.grafana.teams.update_preferences(self.first_team_id, prefs)
        self.assertEqual("Preferences updated", response["message"])

    def test_get_team_external_group(self):
        self.check_external_groups()
        self.grafana.teams.add_team_external_group(self.first_team_id, "group")
        groups = self.grafana.teams.get_team_external_group(self.first_team_id)
        self.assertEqual(groups[0]["groupId"], "group")

    def test_add_team_external_group(self):
        self.check_external_groups()
        response = self.grafana.teams.add_team_external_group(self.first_team_id, "group")
        self.assertEqual("Group added to Team", response["message"])

    def test_remove_team_external_group(self):
        self.check_external_groups()
        self.grafana.teams.add_team_external_group(self.first_team_id, "a_external_group")
        response = self.grafana.teams.remove_team_external_group(self.first_team_id, "a_external_group")
        self.assertEqual("Team group removed", response["message"])

    def check_external_groups(self):
        if Version(self.grafana.version) >= Version("6"):
            pytest.skip("External Group Synchronization is only available in Grafana Enterprise.")
