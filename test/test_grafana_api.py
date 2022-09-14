import os
import unittest
from unittest import mock

import requests

from grafana_client import GrafanaApi, HeaderAuth, TokenAuth


class TestGrafanaApiFactories(unittest.TestCase):
    """
    Test the two factory methods, `GrafanaApi.from_url()`, and
    `GrafanaApi.from_env()`, with different input parameters.
    """

    def test_from_url_default(self):
        grafana = GrafanaApi.from_url()
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "admin")
        self.assertEqual(grafana.client.auth.password, "admin")
        self.assertEqual(grafana.client.url_host, "localhost")
        self.assertEqual(grafana.client.url_port, 3000)
        self.assertEqual(grafana.client.url_path_prefix, "")
        self.assertEqual(grafana.client.url_protocol, "http")
        self.assertEqual(grafana.client.verify, True)
        self.assertEqual(grafana.client.timeout, 5.0)

    def test_from_url_anonymous(self):
        grafana = GrafanaApi.from_url("http://localhost:3000")
        self.assertEqual(grafana.client.auth, None)

    def test_from_url_basicauth(self):
        grafana = GrafanaApi.from_url(credential=("foo", "bar"))
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "foo")
        self.assertEqual(grafana.client.auth.password, "bar")

    def test_from_url_tokenauth(self):
        grafana = GrafanaApi.from_url(credential="VerySecretToken")
        self.assertIsInstance(grafana.client.auth, TokenAuth)
        self.assertEqual(grafana.client.auth.token, "VerySecretToken")

    def test_from_url_headerauth(self):
        grafana = GrafanaApi.from_url(credential=HeaderAuth(name="X-WEBAUTH-USER", value="foobar"))
        self.assertIsInstance(grafana.client.auth, HeaderAuth)
        self.assertEqual(grafana.client.auth.name, "X-WEBAUTH-USER")
        self.assertEqual(grafana.client.auth.value, "foobar")

    def test_from_url_auth_precedence(self):
        grafana = GrafanaApi.from_url("http://foo:bar@localhost:3000", credential="VerySecretToken")
        self.assertIsInstance(grafana.client.auth, TokenAuth)
        self.assertEqual(grafana.client.auth.token, "VerySecretToken")

    def test_from_url_auth_invalid(self):
        self.assertRaises(TypeError, lambda: GrafanaApi.from_url("http://foo:bar@localhost:3000", credential=42.42))

    def test_from_url_full_on(self):
        grafana = GrafanaApi.from_url("https://foo:bar@daq.example.org/grafana/?verify=false")
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "foo")
        self.assertEqual(grafana.client.auth.password, "bar")
        self.assertEqual(grafana.client.url_host, "daq.example.org")
        self.assertEqual(grafana.client.url_port, None)
        self.assertEqual(grafana.client.url_path_prefix, "grafana/")
        self.assertEqual(grafana.client.url_protocol, "https")
        self.assertEqual(grafana.client.verify, False)
        self.assertEqual(grafana.client.timeout, 5.0)

    def test_from_env_default(self):
        grafana = GrafanaApi.from_env()
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "admin")
        self.assertEqual(grafana.client.auth.password, "admin")
        self.assertEqual(grafana.client.url_host, "localhost")
        self.assertEqual(grafana.client.url_port, 3000)
        self.assertEqual(grafana.client.url_path_prefix, "")
        self.assertEqual(grafana.client.url_protocol, "http")
        self.assertEqual(grafana.client.verify, True)
        self.assertEqual(grafana.client.timeout, 5.0)

    @mock.patch.dict(os.environ, {"GRAFANA_URL": "http://localhost:3000"})
    def test_from_env_anonymous(self):
        grafana = GrafanaApi.from_env()
        self.assertEqual(grafana.client.auth, None)

    @mock.patch.dict(os.environ, {"GRAFANA_URL": "http://foo:bar@localhost:3000"})
    def test_from_env_basicauth(self):
        grafana = GrafanaApi.from_env()
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "foo")
        self.assertEqual(grafana.client.auth.password, "bar")

    @mock.patch.dict(os.environ, {"GRAFANA_TOKEN": "VerySecretToken"})
    def test_from_env_tokenauth(self):
        grafana = GrafanaApi.from_env()
        self.assertIsInstance(grafana.client.auth, TokenAuth)
        self.assertEqual(grafana.client.auth.token, "VerySecretToken")

    @mock.patch.dict(os.environ, {"GRAFANA_URL": "http://foo:bar@localhost:3000", "GRAFANA_TOKEN": "VerySecretToken"})
    def test_from_env_auth_precedence(self):
        grafana = GrafanaApi.from_env()
        self.assertIsInstance(grafana.client.auth, TokenAuth)
        self.assertEqual(grafana.client.auth.token, "VerySecretToken")

    @mock.patch.dict(os.environ, {"GRAFANA_URL": "https://foo:bar@daq.example.org/grafana/?verify=false"})
    def test_from_env_full_on(self):
        grafana = GrafanaApi.from_env()
        self.assertIsInstance(grafana.client.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(grafana.client.auth.username, "foo")
        self.assertEqual(grafana.client.auth.password, "bar")
        self.assertEqual(grafana.client.url_host, "daq.example.org")
        self.assertEqual(grafana.client.url_port, None)
        self.assertEqual(grafana.client.url_path_prefix, "grafana/")
        self.assertEqual(grafana.client.url_protocol, "https")
        self.assertEqual(grafana.client.verify, False)
        self.assertEqual(grafana.client.timeout, 5.0)
