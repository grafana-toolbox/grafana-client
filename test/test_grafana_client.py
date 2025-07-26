import unittest
from unittest.mock import Mock, patch

import niquests

from grafana_client.api import GrafanaApi
from grafana_client.client import (
    GrafanaClientError,
    GrafanaServerError,
    GrafanaTimeoutError,
    HeaderAuth,
    TokenAuth,
)


class MockResponse:
    def __init__(self, status_code, headers=None, json_data=None):
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self.json_data = json_data

    def json(self):
        return self.json_data


frontend_settings_buildinfo_payload = {
    "buildInfo": {
        "buildstamp": 1753567501,
        "commit": "e0ba4b480954f8a33aa2cff3229f6bcc05777bd9",
        "commitShort": "e0ba4b4809",
        "edition": "Open Source",
        "env": "production",
        "hasUpdate": True,
        "hideVersion": False,
        "latestVersion": "12.1.0",
        "version": "11.6.2",
        "versionString": "Grafana v11.6.2 (e0ba4b4809)",
    }
}


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

    def test_grafana_client_no_org(self):
        grafana = GrafanaApi(
            ("admin", "admin"), host="localhost", url_path_prefix="", protocol="https", organization_id=None
        )
        self.assertNotIn("X-Grafana-Org-Id", grafana.client.s.headers)

    def test_grafana_client_org(self):
        org_id = 2
        grafana = GrafanaApi(
            ("admin", "admin"), host="localhost", url_path_prefix="", protocol="https", organization_id=org_id
        )
        self.assertEqual(grafana.client.s.headers["X-Grafana-Org-Id"], str(org_id))

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
        grafana.client.s.request = Mock(name="request")
        grafana.client.s.request.return_value = MockResponse(
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

        basic_auth = niquests.auth.HTTPBasicAuth("admin", "admin")
        grafana.users.find_user("test@example.org")
        grafana.client.s.request.assert_called_once_with(
            "get",
            "https://localhost/api/users/lookup?loginOrEmail=test@example.org",
            auth=basic_auth,
            headers=None,
            json=None,
            params=None,
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

        with self.assertRaises(GrafanaTimeoutError):
            grafana.folder.get_all_folders()

    def test_grafana_client_basic_auth(self):
        grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="https", port="3000")
        self.assertTrue(isinstance(grafana.client.auth, niquests.auth.HTTPBasicAuth))

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
        request = niquests.Request()
        tokenauth(request)
        self.assertEqual(request.headers["Authorization"], "Bearer VerySecretToken")

    def test_headerauth(self):
        headerauth = HeaderAuth(name="X-WEBAUTH-USER", value="foobar")
        request = niquests.Request()
        headerauth(request)
        self.assertEqual(request.headers["X-WEBAUTH-USER"], "foobar")

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client_connect_success(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = frontend_settings_buildinfo_payload
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="3000")
        grafana_build_info = grafana.connect()
        self.assertEqual(grafana_build_info["version"], "11.6.2")

    def test_grafana_client_connect_failure(self):
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="32425")
        self.assertRaises(niquests.exceptions.ConnectionError, lambda: grafana.connect())

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client_version_basic(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = frontend_settings_buildinfo_payload
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="3000")
        self.assertEqual(grafana.version, "11.6.2")

    @patch("grafana_client.client.GrafanaClient.__getattr__")
    def test_grafana_client_version_patch(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = {
            "buildInfo": {
                "version": "11.3.0-75420.patch2-75797",
            }
        }
        grafana = GrafanaApi(auth=None, host="localhost", url_path_prefix="", protocol="http", port="3000")
        self.assertEqual(grafana.version, "11.3.0")

    def test_grafana_client_non_json_response(self):
        grafana = GrafanaApi.from_url("https://example.org/")
        self.assertRaises((GrafanaClientError, GrafanaServerError), lambda: grafana.connect())

    def test_grafana_client_204_no_content_response(self):
        grafana = GrafanaApi.from_url()
        grafana.client.s.request = Mock(name="request")
        grafana.client.s.request.return_value = MockResponse(
            status_code=204,
        )
        response = grafana.alertingprovisioning.delete_alertrule("foobar")
        self.assertIsNone(response)
