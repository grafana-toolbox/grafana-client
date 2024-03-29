import unittest

from grafana_client import GrafanaApi

from ..compat import requests_mock


class ServiceAccountsTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/42?accesscontrol=true",
            json={
                "id": 42,
                "name": "rjuan",
                "login": "sa-juan",
                "orgId": 1,
                "isDisabled": False,
                "createdAt": "2023-12-15T21:38:59Z",
                "updatedAt": "2023-12-19T12:46:06Z",
                "avatarUrl": "/avatar/06b4d9db72de4d293813135da09fd736",
                "role": "Viewer",
                "teams": None,
                "accessControl": {
                    "serviceaccounts.permissions:read": True,
                    "serviceaccounts.permissions:write": True,
                    "serviceaccounts:delete": True,
                    "serviceaccounts:read": True,
                    "serviceaccounts:write": True,
                },
            },
        )
        result = self.grafana.serviceaccount.get(42)
        self.assertEqual(
            result,
            {
                "id": 42,
                "name": "rjuan",
                "login": "sa-juan",
                "orgId": 1,
                "isDisabled": False,
                "createdAt": "2023-12-15T21:38:59Z",
                "updatedAt": "2023-12-19T12:46:06Z",
                "avatarUrl": "/avatar/06b4d9db72de4d293813135da09fd736",
                "role": "Viewer",
                "teams": None,
                "accessControl": {
                    "serviceaccounts.permissions:read": True,
                    "serviceaccounts.permissions:write": True,
                    "serviceaccounts:delete": True,
                    "serviceaccounts:read": True,
                    "serviceaccounts:write": True,
                },
            },
        )

    @requests_mock.Mocker()
    def test_create(self, m):
        m.post(
            "http://localhost/api/serviceaccounts/",
            json={"message": "Service account created"},
        )
        user = self.grafana.serviceaccount.create({"name": "foo", "role": "Admin"})
        self.assertEqual(user["message"], "Service account created")

    @requests_mock.Mocker()
    def test_update(self, m):
        m.patch(
            "http://localhost/api/serviceaccounts/42",
            json={"message": "Service account updated"},
        )
        user = self.grafana.serviceaccount.update(42, {"name": "foo", "role": "Admin"})
        self.assertEqual(user["message"], "Service account updated")

    @requests_mock.Mocker()
    def test_delete(self, m):
        m.delete(
            "http://localhost/api/serviceaccounts/42",
            json={"message": "Service account deleted"},
        )
        user = self.grafana.serviceaccount.delete(42)
        self.assertEqual(user["message"], "Service account deleted")

    @requests_mock.Mocker()
    def test_create_token(self, m):
        m.post(
            "http://localhost/api/serviceaccounts/42/tokens",
            json={"message": "Service account token created"},
        )
        user = self.grafana.serviceaccount.create_token(42, {"name": "some-uuid"})
        self.assertEqual(user["message"], "Service account token created")

    @requests_mock.Mocker()
    def test_delete_token(self, m):
        m.delete(
            "http://localhost/api/serviceaccounts/42/tokens/2",
            json={"message": "Service account token deleted"},
        )
        user = self.grafana.serviceaccount.delete_token(42, 2)
        self.assertEqual(user["message"], "Service account token deleted")

    @requests_mock.Mocker()
    def test_get_tokens_some(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/42/tokens",
            json=["token1", "token2"],
        )
        result = self.grafana.serviceaccount.get_tokens(42)
        self.assertEqual(len(result), 2)

    @requests_mock.Mocker()
    def test_get_tokens_zero(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/42/tokens",
            json=[],
        )
        result = self.grafana.serviceaccount.get_tokens(42)
        self.assertEqual(len(result), 0)

    @requests_mock.Mocker()
    def test_search(self, m):
        # TODO: Don't know how the shape of the response looks like.
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=3&perpage=10",
            json={"foo": "bar"},
        )
        result = self.grafana.serviceaccount.search("foo", page=3, perpage=10)
        self.assertEqual(result, [{"foo": "bar"}])

    @requests_mock.Mocker()
    def test_search_one_success(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=1",
            json={"totalCount": 1, "serviceAccounts": [{"foo": "bar"}]},
        )
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=2",
            json={"totalCount": 1, "serviceAccounts": []},
        )
        result = self.grafana.serviceaccount.search_one("foo")
        self.assertEqual(result, {"foo": "bar"})

    @requests_mock.Mocker()
    def test_search_one_find_two(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=1",
            json={"totalCount": 2, "serviceAccounts": [{"foo": "bar"}, {"foo": "baz"}]},
        )
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=2",
            json={"totalCount": 2, "serviceAccounts": []},
        )
        with self.assertRaises(ValueError) as ex:
            self.grafana.serviceaccount.search_one("foo")
        self.assertEqual("More than one service account matched", str(ex.exception))

    @requests_mock.Mocker()
    def test_search_one_find_zero(self, m):
        m.get(
            "http://localhost/api/serviceaccounts/search?query=foo&page=1",
            json={"totalCount": 0, "serviceAccounts": []},
        )
        with self.assertRaises(ValueError) as ex:
            self.grafana.serviceaccount.search_one("foo")
        self.assertEqual("No service account matched", str(ex.exception))
