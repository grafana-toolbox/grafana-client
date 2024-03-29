import unittest

from grafana_client import GrafanaApi

from ..compat import requests_mock


class PluginTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_list(self, m):
        m.get(
            "http://localhost/api/plugins?embedded=0",
            json=[
                {
                    "name": "AWS Data Sources",
                    "type": "app",
                    "id": "aws-datasource-provisioner-app",
                    "enabled": "true",
                    "pinned": "true",
                    "info": {
                        "author": {"name": "Grafana Labs", "url": "https://grafana.com/"},
                        "description": "AWS Datasource Provisioner",
                        "links": [],
                        "logos": {
                            "small": "public/plugins/aws-datasource-provisioner-app/assets/logo-small.svg",
                            "large": "public/plugins/aws-datasource-provisioner-app/assets/logo-large.svg",
                        },
                        "build": {
                            "time": 1684358005873,
                            "repo": "https://github.com/grafana/aws-datasource-provisioner-app",
                            "branch": "main",
                            "hash": "cae4b5ad22e487e9e0f81fca8ed801b36f87c733",
                        },
                        "screenshots": "",
                        "version": "1.8.1",
                        "updated": "2023-05-17",
                    },
                    "dependencies": {"grafanaDependency": ">=7.3.0", "grafanaVersion": ">=7.3.0", "plugins": []},
                    "latestVersion": "",
                    "hasUpdate": "false",
                    "defaultNavUrl": "/plugins/aws-datasource-provisioner-app/page/aws-services",
                    "category": "",
                    "state": "",
                    "signature": "valid",
                    "signatureType": "grafana",
                    "signatureOrg": "Grafana Labs",
                },
                {
                    "name": "AWS IoT SiteWise",
                    "type": "datasource",
                    "id": "grafana-iot-sitewise-datasource",
                    "enabled": "true",
                    "pinned": "false",
                    "info": {
                        "author": {"name": "Grafana Labs", "url": "https://grafana.com"},
                        "description": "A managed service to collect, store, organize and monitor data from industrial "
                        "equipment",
                        "links": [
                            {"name": "Website", "url": "https://aws.amazon.com/iot-sitewise/"},
                            {
                                "name": "Issue Tracker",
                                "url": "https://github.com/grafana/iot-sitewise-datasource/issues",
                            },
                        ],
                        "logos": {
                            "small": "public/plugins/grafana-iot-sitewise-datasource/img/sitewise.svg",
                            "large": "public/plugins/grafana-iot-sitewise-datasource/img/sitewise.svg",
                        },
                        "build": {
                            "time": 1692806526291,
                            "repo": "https://github.com/grafana/iot-sitewise-datasource",
                            "branch": "main",
                            "hash": "a56fdf241cf677e025530d484472a0c838f05b79",
                        },
                        "screenshots": [],
                        "version": "1.11.0",
                        "updated": "2023-08-23",
                    },
                    "dependencies": {"grafanaDependency": ">=8.5.0", "grafanaVersion": "8.5.0", "plugins": []},
                    "latestVersion": "",
                    "hasUpdate": "false",
                    "defaultNavUrl": "/plugins/grafana-iot-sitewise-datasource/",
                    "category": "iot",
                    "state": "",
                    "signature": "unsigned",
                    "signatureType": "",
                    "signatureOrg": "",
                },
                {
                    "name": "AWS IoT TwinMaker App",
                    "type": "app",
                    "id": "grafana-iot-twinmaker-app",
                    "enabled": "true",
                    "pinned": "true",
                    "info": {
                        "author": {"name": "AWS IoT TwinMaker", "url": "https://aws.amazon.com"},
                        "description": "Create end-user 3D digital twin applications to monitor industrial operations "
                        "with AWS IoT TwinMaker. AWS IoT TwinMaker is a service that makes it faster and"
                        "easier for developers to create digital replicas of real-world systems, "
                        "helping more customers realize the potential of digital twins to optimize operations.",
                        "links": [{"name": "Website", "url": "https://github.com/grafana/grafana-iot-twinmaker-app"}],
                        "logos": {
                            "small": "public/plugins/grafana-iot-twinmaker-app/img/AWS-IoT-TwinMaker.png",
                            "large": "public/plugins/grafana-iot-twinmaker-app/img/AWS-IoT-TwinMaker.png",
                        },
                        "build": {
                            "time": 1684967559156,
                            "repo": "https://github.com/grafana/grafana-iot-twinmaker-app",
                            "branch": "main",
                            "hash": "bc9c49f1b66c6146d17667e733b319eae967504b",
                        },
                        "screenshots": [],
                        "version": "1.6.2",
                        "updated": "2023-05-24",
                    },
                    "dependencies": {"grafanaDependency": ">=8.4.0", "grafanaVersion": "8.4.0", "plugins": []},
                    "latestVersion": "",
                    "hasUpdate": "false",
                    "defaultNavUrl": "/plugins/grafana-iot-twinmaker-app/",
                    "category": "iot",
                    "state": "",
                    "signature": "unsigned",
                    "signatureType": "",
                    "signatureOrg": "",
                },
                {
                    "name": "Akumuli",
                    "type": "datasource",
                    "id": "akumuli-datasource",
                    "enabled": "true",
                    "pinned": "false",
                    "info": {
                        "author": {"name": "Eugene Lazin", "url": "https://akumuli.org"},
                        "description": "Datasource plugin for Akumuli time-series database",
                        "links": [{"name": "Project site", "url": "https://github.com/akumuli/Akumuli"}],
                        "logos": {
                            "small": "public/plugins/akumuli-datasource/img/logo.svg.png",
                            "large": "public/plugins/akumuli-datasource/img/logo.svg.png",
                        },
                        "build": {},
                        "screenshots": "",
                        "version": "1.3.12",
                        "updated": "2019-12-19",
                    },
                    "dependencies": {"grafanaDependency": "", "grafanaVersion": "4.5.x", "plugins": []},
                    "latestVersion": "",
                    "hasUpdate": "false",
                    "defaultNavUrl": "/plugins/akumuli-datasource/",
                    "category": "",
                    "state": "",
                    "signature": "unsigned",
                    "signatureType": "",
                    "signatureOrg": "",
                },
                {
                    "name": "Alert list",
                    "type": "panel",
                    "id": "alertlist",
                    "enabled": "true",
                    "pinned": "false",
                    "info": {
                        "author": {"name": "Grafana Labs", "url": "https://grafana.com"},
                        "description": "Shows list of alerts and their current status",
                        "links": "null",
                        "logos": {
                            "small": "public/app/plugins/panel/alertlist/img/icn-singlestat-panel.svg",
                            "large": "public/app/plugins/panel/alertlist/img/icn-singlestat-panel.svg",
                        },
                        "build": {},
                        "screenshots": "null",
                        "version": "",
                        "updated": "",
                    },
                    "dependencies": {"grafanaDependency": "", "grafanaVersion": "*", "plugins": []},
                    "latestVersion": "",
                    "hasUpdate": "false",
                    "defaultNavUrl": "/plugins/alertlist/",
                    "category": "",
                    "state": "",
                    "signature": "internal",
                    "signatureType": "",
                    "signatureOrg": "",
                },
            ],
        )
        plugins = self.grafana.plugin.list()
        self.assertTrue(len(plugins), 6)

    @requests_mock.Mocker()
    def test_install(self, m):
        m.post(
            "http://localhost/api/plugins/alertlist/install",
            json={"message": "Plugin alertlist installed"},
        )
        response = self.grafana.plugin.install(plugin_id="alertlist", version="1.3.12")
        self.assertEqual(response["message"], "Plugin alertlist installed")

    @requests_mock.Mocker()
    def test_uninstall(self, m):
        m.post(
            "http://localhost/api/plugins/alertlist/uninstall",
            json={"message": "Plugin alertlist uninstalled"},
        )
        response = self.grafana.plugin.uninstall(plugin_id="alertlist")
        self.assertEqual(response["message"], "Plugin alertlist uninstalled")

    @requests_mock.Mocker()
    def test_health(self, m):
        m.get(
            "http://localhost/api/plugins/alertlist/health",
            json={"message": "Plugin alertlist healthy"},
        )
        response = self.grafana.plugin.health(plugin_id="alertlist")
        self.assertEqual(response["message"], "Plugin alertlist healthy")

    @requests_mock.Mocker()
    def test_metrics(self, m):
        m.get(
            "http://localhost/api/plugins/grafana-timestream-datasource/metrics",
            json={"message": "Not found"},
        )
        response = self.grafana.plugin.metrics(plugin_id="grafana-timestream-datasource")
        self.assertEqual(response["message"], "Not found")
