import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError, GrafanaServerError

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class PluginTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi):
        self.grafana = grafana_api
        self.plugin_id = "marcusolsson-hourly-heatmap-panel"

        if Version(self.grafana.version) < Version("8"):
            pytest.skip("Testing plugins only supported on Grafana 8 and higher.")

    def test_list(self):
        plugins = self.grafana.plugin.list()
        self.assertGreaterEqual(len(plugins), 6)

    def test_install_success(self):
        self.install_plugin(plugin_id=self.plugin_id)

    def test_install_collision_core(self):
        """Validate installation collision with core plugin"""
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.plugin.install(plugin_id="text", version="0.8.15")
        self.assertEqual(403, context.exception.status_code, "Wrong status code")
        self.assertIn("Cannot install or change a Core plugin", context.exception.message)

    def test_uninstall_success(self):
        self.install_plugin(plugin_id=self.plugin_id)
        self.grafana.plugin.uninstall(plugin_id=self.plugin_id)

    def test_uninstall_core(self):
        """Validate uninstallation of core plugin fails"""
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.plugin.uninstall(plugin_id="text")
        self.assertEqual(403, context.exception.status_code, "Wrong status code")
        self.assertIn("Cannot uninstall a Core plugin", context.exception.message)

    def test_uninstall_unknown(self):
        """Validate uninstallation of non-existent plugin fails"""
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.plugin.uninstall(plugin_id="unknown")
        self.assertEqual(404, context.exception.status_code, "Wrong status code")
        self.assertIn("Plugin not installed", context.exception.message)

    def test_health_success(self):
        """Validate health check after installing plugin"""
        if Version(self.grafana.version) < Version("10"):
            pytest.skip("grafana-testdata-datasource not available on Grafana 9 and before")
        response = self.grafana.plugin.health(plugin_id="grafana-testdata-datasource")
        self.assertEqual("Data source is working", response["message"])

    def test_health_core(self):
        """Standard core plugins can't do health checks by default"""
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.plugin.health(plugin_id="text")
        if Version(self.grafana.version) >= Version("10"):
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("Plugin unavailable", context.exception.message)
        else:
            self.assertEqual(503, context.exception.status_code, "Wrong status code")
            self.assertIn("Plugin unavailable", context.exception.message)

    def test_health_unknown(self):
        """Validate failing health check on non-existent plugin"""
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.plugin.health(plugin_id="unknown")
        self.assertEqual(404, context.exception.status_code, "Wrong status code")
        self.assertRegex(context.exception.message, "(Plugin not found|Plugin not registered)")

    def test_metrics_success(self):
        plugin_id = "grafana-github-datasource"
        self.install_plugin(plugin_id=plugin_id)
        response = self.grafana.plugin.metrics(plugin_id=plugin_id)
        self.assertIn("process_virtual_memory_max_bytes", response)

    def test_metrics_not_implemented(self):
        with self.assertRaises(GrafanaServerError) as context:
            self.grafana.plugin.metrics(plugin_id="text")
        if Version(self.grafana.version) >= Version("10"):
            self.assertEqual(500, context.exception.status_code, "Wrong status code")
            self.assertIn("An error occurred within the plugin", context.exception.message)
        else:
            self.assertEqual(503, context.exception.status_code, "Wrong status code")
            self.assertIn("Plugin unavailable", context.exception.message)

    def test_metrics_unknown(self):
        with self.assertRaises(GrafanaClientError) as context:
            self.grafana.plugin.metrics(plugin_id="unknown")
        self.assertEqual(404, context.exception.status_code, "Wrong status code")
        if Version(self.grafana.version) >= Version("10"):
            self.assertIn("Plugin not registered", context.exception.message)
        else:
            self.assertIn("Plugin not found", context.exception.message)

    def install_plugin(self, plugin_id: str):
        try:
            self.grafana.plugin.by_id(plugin_id=plugin_id)
            return
        except KeyError as ex:
            if "Plugin not found" not in str(ex):
                raise
        self.grafana.plugin.install(plugin_id=plugin_id)
