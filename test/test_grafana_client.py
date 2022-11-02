import sys
import unittest

if sys.version_info > (3, 0):
    from unittest.mock import Mock, patch
else:
    from mock import patch, Mock

import requests

from grafana_client.api import GrafanaApi
from grafana_client.client import GrafanaClientError, HeaderAuth, TokenAuth


class MockResponse:
    def __init__(self, status_code, headers=None, json_data=None):
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self.json_data = json_data

    def json(self):
        return self.json_data


class TestGrafanaClient(unittest.TestCase):
    def test_grafana_client_user_agent_default(self):
        grafana = GrafanaApi.from_url()

        from grafana_client import __appname__, __version__

        user_agent = f"{__appname__}/{__version__}"

        self.assertTrue(user_agent.startswith("grafana-client"))
        self.assertEqual(grafana.client.s.headers["User-Agent"], user_agent)

    def test_grafana_client_user_agent_custom(self):
        grafana = GrafanaApi(
            ("admin", "admin"), host="localhost", url_path_prefix="", protocol="https", user_agent="foobar/3000"
        )
        self.assertEqual(grafana.client.s.headers["User-Agent"], "foobar/3000")

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = """{
  "email": "user@mygraf.com",
  "name": "admin",
  "login": "admin",
  "theme": "light",
  "orgId": 1,
  "isGrafanaAdmin": true
}"""
        grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="https")
        grafana.users.find_user("test@example.org")

    def test_grafana_client_no_verify(self):
        grafana = GrafanaApi(
            ("admin", "admin"),
            host="localhost",
            url_path_prefix="",
            protocol="https",
            verify=False,
        )
        grafana.client.s.get = Mock(name="get")
        grafana.client.s.get.return_value = MockResponse(
            status_code=200,
            json_data={
                "email": "user@mygraf.com",
                "name": "admin",
                "login": "admin",
                "theme": "light",
                "orgId": 1,
                "isGrafanaAdmin": True,
            },
        )

        basic_auth = requests.auth.HTTPBasicAuth("admin", "admin")
        grafana.users.find_user("test@example.org")
        grafana.client.s.get.assert_called_once_with(
            "https://localhost/api/users/lookup?loginOrEmail=test@example.org",
            auth=basic_auth,
            headers=None,
            json=None,
            data=None,
            verify=False,
            timeout=5.0,
        )

    def test_grafana_client_timeout(self):
        grafana = GrafanaApi(
            ("admin", "admin"),
            host="play.grafana.org",
            url_path_prefix="",
            protocol="https",
            verify=False,
            timeout=0.0001,
        )

        with self.assertRaises(requests.exceptions.Timeout):
            grafana.folder.get_all_folders()

    def test_grafana_client_basic_auth(self):
        grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="https", port="3000")
        self.assertTrue(isinstance(grafana.client.auth, requests.auth.HTTPBasicAuth))

    def test_grafana_client_token_auth(self):
        grafana = GrafanaApi(
            "alongtoken012345etc",
            host="localhost",
            url_path_prefix="",
            protocol="https",
        )
        self.assertTrue(isinstance(grafana.client.auth, TokenAuth))

    def test_tokenauth(self):
        tokenauth = TokenAuth("VerySecretToken")
        request = requests.Request()
        tokenauth(request)
        self.assertEqual(request.headers["Authorization"], "Bearer VerySecretToken")

    def test_headerauth(self):
        headerauth = HeaderAuth(name="X-WEBAUTH-USER", value="foobar")
        request = requests.Request()
        headerauth(request)
        self.assertEqual(request.headers["X-WEBAUTH-USER"], "foobar")

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client_connect_success(self, mock_get):
        payload = {"commit": "14e988bd22", "database": "ok", "version": "9.0.1"}
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = payload
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="3000")
        grafana_info = grafana.connect()
        self.assertEqual(grafana_info, payload)

    def test_grafana_client_connect_failure(self):
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="32425")
        self.assertRaises(requests.exceptions.ConnectionError, lambda: grafana.connect())

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client_version(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = {"commit": "14e988bd22", "database": "ok", "version": "9.0.1"}
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="3000")
        self.assertEqual(grafana.version, "9.0.1")

    def test_grafana_client_non_json_response(self):
        grafana = GrafanaApi.from_url("https://httpbin.org/html")
        self.assertRaises(GrafanaClientError, lambda: grafana.connect())

    def test_grafana_client_204_no_content_response(self):
        grafana = GrafanaApi.from_url()
        grafana.client.s.delete = Mock(name="get")
        grafana.client.s.delete.return_value = MockResponse(
            status_code=204,
        )
        response = grafana.alertingprovisioning.delete_alertrule("foobar")
        assert response is None
