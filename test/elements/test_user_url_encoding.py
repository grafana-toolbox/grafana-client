"""
User API parameters need to be URL-encoded before being interpolated into the request path.

https://github.com/grafana-toolbox/grafana-client/issues/247
"""

import sys
import unittest

import pytest

from grafana_client import GrafanaApi

from ..compat import requests_mock

if "pytest" in sys.argv[0]:
    pytest.skip("Skipping pytest, please use unittest", allow_module_level=True)


class UserUrlEncodingTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_find_user_encodes_login_or_email(self, m):
        m.get(requests_mock.ANY, json={"id": 1, "login": "test+2@example.com"})
        self.grafana.users.find_user("test+2@example.com")
        self.assertEqual(
            "http://localhost/api/users/lookup?loginOrEmail=test%2B2%40example.com",
            m.last_request.url,
        )

    @requests_mock.Mocker()
    def test_search_users_encodes_query(self, m):
        m.get(requests_mock.ANY, json=[])
        self.grafana.users.search_users("test+2@example.com", page=1)
        self.assertEqual(
            "http://localhost/api/users?query=test%2B2%40example.com&page=1",
            m.last_request.url,
        )
