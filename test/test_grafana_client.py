import sys
import unittest

if sys.version_info > (3, 0):
    from unittest.mock import Mock, patch
else:
    from mock import patch, Mock

import requests

from grafana_client.api import GrafanaApi
from grafana_client.client import TokenAuth


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestGrafanaClient(unittest.TestCase):
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
            {
                "email": "user@mygraf.com",
                "name": "admin",
                "login": "admin",
                "theme": "light",
                "orgId": 1,
                "isGrafanaAdmin": True,
            },
            200,
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


if __name__ == "__main__":
    import xmlrunner

    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
