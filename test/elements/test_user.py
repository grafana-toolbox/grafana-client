import unittest

from grafana_client import GrafanaApi
from grafana_client.model import PersonalPreferences

from ..compat import requests_mock


class UsersTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_update_user(self, m):
        m.put(
            "http://localhost/api/users/foo",
            json={},
            headers={"Content-Type": "application/json"},
        )
        user = self.grafana.users.update_user("foo", {})
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_get_user(self, m):
        m.get(
            "http://localhost/api/users/foo",
            json={},
            headers={"Content-Type": "application/json"},
        )
        user = self.grafana.users.get_user("foo")
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_find_user(self, m):
        m.get(
            "http://localhost/api/users/lookup?loginOrEmail=foo",
            json={},
            headers={"Content-Type": "application/json"},
        )
        user = self.grafana.users.find_user("foo")
        self.assertEqual(user, {})

    @requests_mock.Mocker()
    def test_search_users_default(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1",
            json=[{"name": "foo"}, {"name": "bar"}],
            headers={"Content-Type": "application/json"},
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2",
            json=[],
            headers={"Content-Type": "application/json"},
        )
        users = self.grafana.users.search_users("foo")
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_search_users_default_empty(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1",
            json=[],
            headers={"Content-Type": "application/json"},
        )
        users = self.grafana.users.search_users("foo")
        self.assertEqual(len(users), 0)

    @requests_mock.Mocker()
    def test_search_users_page2(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=2",
            json=[{}],
            headers={"Content-Type": "application/json"},
        )
        users = self.grafana.users.search_users("foo", page=2)
        self.assertEqual(users, [{}])

    @requests_mock.Mocker()
    def test_search_users_perpage(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1&perpage=1",
            json=[{"name": "foo"}, {"name": "bar"}],
            headers={"Content-Type": "application/json"},
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2&perpage=1",
            json=[],
            headers={"Content-Type": "application/json"},
        )
        users = self.grafana.users.search_users("foo", perpage=1)
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_search_users_perpage_no_endless_loop(self, m):
        m.get(
            "http://localhost/api/users?query=foo&page=1&perpage=5",
            json=[{"name": "foo"}, {"name": "bar"}],
            headers={"Content-Type": "application/json"},
        )
        m.get(
            "http://localhost/api/users?query=foo&page=2&perpage=5",
            json=[],
            headers={"Content-Type": "application/json"},
        )
        users = self.grafana.users.search_users("foo", perpage=5)
        self.assertEqual(len(users), 2)

    @requests_mock.Mocker()
    def test_get_user_organisations(self, m):
        m.get(
            "http://localhost/api/users/foo/orgs",
            json=[],
            headers={"Content-Type": "application/json"},
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
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.get_actual_user()
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_change_actual_user_password(self, m):
        m.put(
            "http://localhost/api/user/password",
            json={},
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.change_actual_user_password("old", "new")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_switch_user_organisation(self, m):
        m.post(
            "http://localhost/api/users/foo/using/acme",
            json={},
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.switch_user_organisation("foo", "acme")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_switch_actual_user_organisation(self, m):
        m.post(
            "http://localhost/api/user/using/acme",
            json={},
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.switch_actual_user_organisation("acme")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_get_actual_user_organisations(self, m):
        m.get(
            "http://localhost/api/user/orgs",
            json=[],
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.get_actual_user_organisations()
        self.assertEqual(result, [])

    @requests_mock.Mocker()
    def test_star_actual_user_dashboard(self, m):
        m.post(
            "http://localhost/api/user/stars/dashboard/987vb7t33",
            json={},
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.star_actual_user_dashboard("987vb7t33")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_unstar_actual_user_dashboard(self, m):
        m.delete(
            "http://localhost/api/user/stars/dashboard/987vb7t33",
            json={},
            headers={"Content-Type": "application/json"},
        )
        result = self.grafana.user.unstar_actual_user_dashboard("987vb7t33")
        self.assertEqual(result, {})

    @requests_mock.Mocker()
    def test_get_preferences(self, m):
        m.get(
            "http://localhost/api/user/preferences",
            json={"theme": "", "homeDashboardId": 0, "timezone": ""},
            headers={"Content-Type": "application/json"},
        )

        result = self.grafana.user.get_preferences()
        self.assertEqual(result["homeDashboardId"], 0)

    @requests_mock.Mocker()
    def test_update_preferences(self, m):
        m.put(
            "http://localhost/api/user/preferences",
            json={"message": "Preferences updated"},
            headers={"Content-Type": "application/json"},
        )
        preference = self.grafana.user.update_preferences(
            PersonalPreferences(theme="", homeDashboardId=999, timezone="utc")
        )
        self.assertEqual(preference["message"], "Preferences updated")

    @requests_mock.Mocker()
    def test_patch_preferences(self, m):
        m.patch(
            "http://localhost/api/user/preferences",
            json={"message": "Preferences updated"},
            headers={"Content-Type": "application/json"},
        )
        preference = self.grafana.user.patch_preferences(PersonalPreferences(homeDashboardUID="zgjG8dKVz"))
        self.assertEqual(preference["message"], "Preferences updated")
