import unittest

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.model import PersonalPreferences


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_update_user(self, m):
        m.put(
            "http://localhost/api/users/foo",
            json={},
        )
        user = self.grafana.users.update_user("foo", {})
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_get_user(self, m):
        m.get(
            "http://localhost/api/users/foo",
            json={},
        )
        user = self.grafana.users.get_user("foo")
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_find_user(self, m):
        m.get(
            "http://localhost/api/users/lookup?loginOrEmail=foo",
            json={},
        )
        user = self.grafana.users.find_user("foo")
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_search_users_default(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1",
            json=[{"name": "foo"}, {"name": "bar"}],
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2",
            json=[],
        )
        users = self.grafana.users.search_users("foo")
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_search_users_default_empty(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1",
            json=[],
        )
        users = self.grafana.users.search_users("foo")
        self.assertEqual(len(users), 0)

    @requests_mock.Mocker()
    def test_search_users_page2(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=2",
            json=[{}],
        )
        users = self.grafana.users.search_users("foo", page=2)
        self.assertEqual(users, [{}])

    @requests_mock.Mocker()
    def test_search_users_perpage(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1&perpage=1",
            json=[{"name": "foo"}, {"name": "bar"}],
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2&perpage=1",
            json=[],
        )
        users = self.grafana.users.search_users("foo", perpage=1)
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_search_users_perpage_no_endless_loop(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1&perpage=5",
            json=[{"name": "foo"}, {"name": "bar"}],
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2&perpage=5",
            json=[],
        )
        users = self.grafana.users.search_users("foo", perpage=5)
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_get_user_organisations(self, m):
        m.get(
            "http://localhost/api/users/foo/orgs",
            json=[],
        )
        users = self.grafana.users.get_user_organisations("foo")
        self.assertEqual(users, [])


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_actual_user(self, m):
        m.get(
            "http://localhost/api/user",
            json={},
        )
        result = self.grafana.user.get_actual_user()
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_change_actual_user_password(self, m):
        m.put(
            "http://localhost/api/user/password",
            json={},
        )
        result = self.grafana.user.change_actual_user_password("old", "new")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_switch_user_organisation(self, m):
        m.post(
            "http://localhost/api/users/foo/using/acme",
            json={},
        )
        result = self.grafana.user.switch_user_organisation("foo", "acme")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_switch_actual_user_organisation(self, m):
        m.post(
            "http://localhost/api/user/using/acme",
            json={},
        )
        result = self.grafana.user.switch_actual_user_organisation("acme")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_get_actual_user_organisations(self, m):
        m.get(
            "http://localhost/api/user/orgs",
            json=[],
        )
        result = self.grafana.user.get_actual_user_organisations()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_star_actual_user_dashboard(self, m):
        m.post(
            "http://localhost/api/user/stars/dashboard/987vb7t33",
            json={},
        )
        result = self.grafana.user.star_actual_user_dashboard("987vb7t33")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_unstar_actual_user_dashboard(self, m):
        m.delete(
            "http://localhost/api/user/stars/dashboard/987vb7t33",
            json={},
        )
        result = self.grafana.user.unstar_actual_user_dashboard("987vb7t33")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_get_preferences(self, m):
        m.get("http://localhost/api/user/preferences", json={"theme": "", "homeDashboardId": 0, "timezone": ""})

        result = self.grafana.user.get_preferences()
        self.assertEqual(result["homeDashboardId"], 0)

    @requests_mock.Mocker()
    def test_update_preferences(self, m):
        m.put("http://localhost/api/user/preferences", json={"message": "Preferences updated"})
        preference = self.grafana.user.update_preferences(
            PersonalPreferences(theme="", homeDashboardId=999, timezone="utc")
        )
        self.assertEqual(preference["message"], "Preferences updated")

    @requests_mock.Mocker()
    def test_patch_preferences(self, m):
        m.patch("http://localhost/api/user/preferences", json={"message": "Preferences updated"})
        preference = self.grafana.user.patch_preferences(PersonalPreferences(homeDashboardUID="zgjG8dKVz"))
        self.assertEqual(preference["message"], "Preferences updated")
