import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError, GrafanaClientError
from grafana_client.elements import LibraryElement

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class LibraryElementTestCase(unittest.TestCase):
    MissingPanelUID: str = "missing-panel"
    MissingPanelName: str = "Unknown name"

    ConnectedPanelUID: str = "856140aa-7548-43fc-9b27-721998bb4152"
    ConnectedPanelName: str = "CPU Seconds"
    ConnectedPanelJSON: dict = {
        "id": 2,
        "kind": 1,
        "meta": {"connectedDashboards": 2},
        "model": {
            "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 1},
            "id": 1,
            "libraryPanel": {"name": "CPU Seconds", "uid": "cec85d6f-834b-427e-8993-562d34fff5c4"},
            "targets": [
                {
                    "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
                    "disableTextWrap": False,
                    "editorMode": "builder",
                    "expr": 'rate(process_cpu_seconds_total{job=~"$Job", instance=~"$Instance"}[$__rate_interval])',
                    "fullMetaSearch": False,
                    "includeNullMetadata": True,
                    "instant": False,
                    "legendFormat": "__auto",
                    "range": True,
                    "refId": "A",
                    "useBackend": False,
                }
            ],
            "title": "CPU Seconds",
            "type": "timeseries",
        },
        "name": "CPU Seconds",
        "orgId": 1,
        "type": "timeseries",
        "uid": "856140aa-7548-43fc-9b27-721998bb4152",
        "version": 1,
    }
    ConnectedPanelConnectionUIDs: list = (
        "de3791ac-6079-4c18-bde0-cb390c079722",
        "a45fbfd0-b211-45fc-96ae-a56886075948",
    )
    ConnectedPanelConnectionsJSON: dict = {
        "result": [
            {
                "id": 2,
                "kind": 1,
                "elementId": 2,
                "connectionId": 101,
                "connectionUid": "de3791ac-6079-4c18-bde0-cb390c079722",
                "created": "2024-02-06T12:19:14-06:00",
                "createdBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
            },
            {
                "id": 5,
                "kind": 1,
                "elementId": 2,
                "connectionId": 102,
                "connectionUid": "a45fbfd0-b211-45fc-96ae-a56886075948",
                "created": "2024-02-06T13:21:12-06:00",
                "createdBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
            },
        ]
    }

    UnconnectedPanelUID: str = "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6"
    UnconnectedPanelName: str = "Heap Memory"
    UnconnectedPanelConnectionsJSON: dict = {"result": []}
    UnconnectedPanelJSON: dict = {
        "id": 3,
        "kind": 1,
        "meta": {},
        "model": {
            "datasource": {"type": "prometheus", "uid": "fb5e0357-258c-4831-b447-565be35828b5"},
            "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
            "id": 3,
            "libraryPanel": {"name": "Heap Memory", "uid": "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6"},
            "targets": [
                {
                    "datasource": {"type": "prometheus", "uid": "fb5e0357-258c-4831-b447-565be35828b5"},
                    "disableTextWrap": False,
                    "editorMode": "builder",
                    "expr": 'jvm_memory_bytes_committed{job=~"$Job", instance=~"$Instance", area="heap"}',
                    "fullMetaSearch": False,
                    "includeNullMetadata": True,
                    "instant": False,
                    "legendFormat": "Committed",
                    "range": True,
                    "refId": "A",
                    "useBackend": False,
                },
                {
                    "datasource": {"type": "prometheus", "uid": "fb5e0357-258c-4831-b447-565be35828b5"},
                    "disableTextWrap": False,
                    "editorMode": "builder",
                    "expr": 'jvm_memory_bytes_used{job=~"$Job", instance=~"$Instance", area="heap"}',
                    "fullMetaSearch": False,
                    "hide": False,
                    "includeNullMetadata": True,
                    "instant": False,
                    "legendFormat": "Used",
                    "range": True,
                    "refId": "B",
                    "useBackend": False,
                },
                {
                    "datasource": {"type": "prometheus", "uid": "fb5e0357-258c-4831-b447-565be35828b5"},
                    "disableTextWrap": False,
                    "editorMode": "builder",
                    "expr": 'jvm_memory_bytes_max{job=~"$Job", instance=~"$Instance", area="heap"}',
                    "fullMetaSearch": False,
                    "hide": False,
                    "includeNullMetadata": True,
                    "instant": False,
                    "legendFormat": "Max",
                    "range": True,
                    "refId": "C",
                    "useBackend": False,
                },
            ],
            "title": "Heap Memory",
            "type": "timeseries",
        },
        "name": "Heap Memory",
        "orgId": 1,
        "type": "timeseries",
        "uid": "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6",
        "version": 1,
    }

    CreatePanelUID: str = "cec85d6f-834b-427e-8993-562d34fff5c4"
    CreatePanelName: str = "CPU Seconds"
    CreatePanelModelJSON: dict = {
        "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
        "description": "",
        "fieldConfig": {
            "defaults": {
                "color": {"mode": "palette-classic"},
                "custom": {
                    "axisBorderShow": False,
                    "axisCenteredZero": False,
                    "axisColorMode": "text",
                    "axisLabel": "",
                    "axisPlacement": "auto",
                    "barAlignment": 0,
                    "drawStyle": "line",
                    "fillOpacity": 0,
                    "gradientMode": "none",
                    "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                    "insertNulls": False,
                    "lineInterpolation": "linear",
                    "lineWidth": 1,
                    "pointSize": 5,
                    "scaleDistribution": {"type": "linear"},
                    "showPoints": "auto",
                    "spanNulls": False,
                    "stacking": {"group": "A", "mode": "none"},
                    "thresholdsStyle": {"mode": "off"},
                },
                "mappings": [],
                "thresholds": {
                    "mode": "absolute",
                    "steps": [{"color": "green", "value": None}, {"color": "red", "value": 80}],
                },
                "unit": "s",
            },
            "overrides": [],
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 1},
        "libraryPanel": {"name": "CPU Seconds", "uid": "cec85d6f-834b-427e-8993-562d34fff5c4"},
        "options": {
            "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": False},
            "tooltip": {"mode": "multi", "sort": "none"},
        },
        "targets": [
            {
                "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
                "disableTextWrap": False,
                "editorMode": "builder",
                "expr": 'rate(process_cpu_seconds_total{job=~"$Job", instance=~"$Instance"}[$__rate_interval])',
                "fullMetaSearch": False,
                "includeNullMetadata": True,
                "instant": False,
                "legendFormat": "__auto",
                "range": True,
                "refId": "A",
                "useBackend": False,
            }
        ],
        "title": "CPU Seconds",
        "transparent": True,
        "type": "timeseries",
    }

    UpdatePanelUID: str = "cec85d6f-834b-427e-8993-562d34fff5c4"
    UpdatePanelName: str = "CPU Seconds"
    UpdatePanelModelJSON: dict = {
        "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
        "gridPos": {"h": 8, "w": 12, "x": 10, "y": 15},
        "id": 1,
        "libraryPanel": {"name": "CPU Seconds", "uid": "cec85d6f-834b-427e-8993-562d34fff5c4"},
        "targets": [
            {
                "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
                "disableTextWrap": False,
                "editorMode": "builder",
                "expr": 'rate(process_cpu_seconds_total{job=~"$Job", instance=~"$Instance"}[$__rate_interval])',
                "fullMetaSearch": False,
                "includeNullMetadata": True,
                "instant": False,
                "legendFormat": "__auto",
                "range": True,
                "refId": "A",
                "useBackend": False,
            }
        ],
        "title": "CPU Seconds",
        "type": "timeseries",
    }

    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi, dashboard_uid: str, dashboard_id: str, folder_uid: str):
        self.grafana = grafana_api
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Testing support library elements only supported on Grafana 9 and higher.")

        # FIXME: How to enable library use with Grafana 12 when `create_rbac_role` does not work on Grafana OSS?
        #        Is there an environment variable that unlocks it, possibly similar like `GF_USERS_ALLOW_ORG_CREATE`?
        #        ERROR: grafana_client.client.GrafanaClientError: Client Error 403: You'll need additional
        #               permissions to perform this action. Permissions needed: library.panels:delete
        if Version(self.grafana.version) >= Version("12"):
            pytest.skip("FIXME: Permissions needed for Grafana 12: library.panels:delete.")

        self.dashboard_id = dashboard_id
        self.dashboard_uid = dashboard_uid
        self.folder_uid = folder_uid

        """
        # Client Error 404: Not found
        self.grafana.rbac.create_rbac_role({
            "name": "library.panels:delete",
            "global": True,
            "permissions": [
                {
                    "action": "library.panels:delete",
                    "scope": "permissions:type:delegate"
                }
            ]
        })
        """

        # Prune all library elements.
        for uuid in [
            LibraryElementTestCase.CreatePanelUID,
            LibraryElementTestCase.ConnectedPanelUID,
            LibraryElementTestCase.UnconnectedPanelUID,
        ]:
            try:
                self.grafana.libraryelement.delete_library_element(uuid)
            except GrafanaClientError as ex:
                if ex.status_code != 404:
                    raise

        # Provision library elements.
        self.grafana.libraryelement.create_library_element(
            model=self.ConnectedPanelJSON,
            name=self.ConnectedPanelName,
            uid=self.ConnectedPanelUID,
            kind=LibraryElement.Panel,
        )
        self.grafana.libraryelement.create_library_element(
            model=LibraryElementTestCase.CreatePanelModelJSON,
            name=LibraryElementTestCase.CreatePanelName,
            uid=LibraryElementTestCase.CreatePanelUID,
            kind=LibraryElement.Panel,
            folder_uid=self.folder_uid,
        )

    def test_get_library_element_success(self):
        response = self.grafana.libraryelement.get_library_element(LibraryElementTestCase.ConnectedPanelUID)
        element = response["result"]
        self.assertEqual(element["uid"], LibraryElementTestCase.ConnectedPanelUID)

    def test_get_library_element_notfound(self):
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    def test_get_library_element_by_name_success(self):
        response = self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.ConnectedPanelName)
        element = response["result"][0]
        self.assertEqual(element["name"], LibraryElementTestCase.ConnectedPanelName)

    def test_get_library_element_by_name_notfound(self):
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.MissingPanelName)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @pytest.mark.skip(reason="FIXME: How to provision `ConnectedPanelConnectionsJSON` to Grafana?")
    def test_get_library_element_connections_success(self):
        # TODO: Provision step for `ConnectedPanelConnectionsJSON` is missing.
        connections = self.grafana.libraryelement.get_library_element_connections(
            LibraryElementTestCase.ConnectedPanelUID
        )
        self.assertEqual(len(connections["result"]), 2)
        self.assertIn(connections["result"][0]["connectionUid"], LibraryElementTestCase.ConnectedPanelConnectionUIDs)
        self.assertIn(connections["result"][1]["connectionUid"], LibraryElementTestCase.ConnectedPanelConnectionUIDs)

    def test_get_library_element_connections_notfound(self):
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element_connections(LibraryElementTestCase.MissingPanelUID)
        if Version(self.grafana.version) >= Version("12"):
            self.assertEqual(403, ex.exception.status_code)
            self.assertRegex(ex.exception.message, "Client Error 403:.*Permissions needed: library.panels:read")
        else:
            self.assertEqual(404, ex.exception.status_code)
            self.assertEqual(ex.exception.message, "Client Error 404: library element could not be found")

    def test_get_library_element_connections_noconnections(self):
        # TODO: Provisioning step for `UnconnectedPanelConnectionsJSON` is missing.
        self.grafana.libraryelement.create_library_element(
            self.UnconnectedPanelJSON,
            name=self.UnconnectedPanelName,
            uid=self.UnconnectedPanelUID,
            kind=LibraryElement.Panel,
        )
        connections = self.grafana.libraryelement.get_library_element_connections(
            LibraryElementTestCase.UnconnectedPanelUID
        )
        self.assertEqual(len(connections["result"]), 0)

    def test_create_library_element_already_exists(self):
        with self.assertRaisesRegex(
            GrafanaBadInputError, "Bad Input: .*library element with that name or UID already exists.*"
        ):
            self.grafana.libraryelement.create_library_element(
                model=LibraryElementTestCase.CreatePanelModelJSON,
                name=LibraryElementTestCase.CreatePanelName,
                uid=LibraryElementTestCase.CreatePanelUID,
                folder_uid=self.folder_uid,
            )

    def test_update_library_element_success(self):
        resp = self.grafana.libraryelement.update_library_element(
            model=LibraryElementTestCase.UpdatePanelModelJSON,
            name=LibraryElementTestCase.UpdatePanelName,
            uid=LibraryElementTestCase.UpdatePanelUID,
            folder_uid=self.folder_uid,
            version=1,
        )
        self.assertIsNotNone(resp["result"])
        self.assertIsNotNone(resp["result"]["folderUid"])
        self.assertEqual(resp["result"]["folderUid"], self.folder_uid)
        self.assertIsNotNone(resp["result"]["uid"])
        self.assertEqual(resp["result"]["uid"], LibraryElementTestCase.CreatePanelUID)
        self.assertIsNotNone(resp["result"]["model"])
        self.assertIsNotNone(resp["result"]["model"]["gridPos"])
        self.assertIsNotNone(resp["result"]["model"]["gridPos"]["x"])
        self.assertEqual(resp["result"]["model"]["gridPos"]["x"], 10)
        self.assertIsNotNone(resp["result"]["model"]["gridPos"]["y"])
        self.assertEqual(resp["result"]["model"]["gridPos"]["y"], 15)
        self.assertIsNotNone(resp["result"]["version"])
        self.assertEqual(resp["result"]["version"], 2)

    def test_update_library_element_notfound(self):
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.update_library_element(
                model=LibraryElementTestCase.UpdatePanelModelJSON,
                name=LibraryElementTestCase.UpdatePanelName,
                uid=LibraryElementTestCase.MissingPanelUID,
                folder_uid=self.folder_uid,
                version=1,
            )
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @pytest.mark.skip(reason="FIXME: How to provision `ConnectedPanelConnectionsJSON` to Grafana?")
    def test_delete_library_element_connections(self):
        # TODO: Provision step for `ConnectedPanelConnectionsJSON` is missing.
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.ConnectedPanelUID)
        self.assertEqual(403, ex.exception.status_code)
        self.assertEqual("Client Error 403: the library element has connections", ex.exception.message)

    def test_delete_library_element_noconnections(self):
        resp = self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.CreatePanelUID)
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp.get("message"))
        self.assertEqual("Library element deleted", resp.get("message"))

    def test_delete_library_element_notfound(self):
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    def test_list_library_elements(self):
        elements = self.grafana.libraryelement.list_library_elements()
        self.assertIsNotNone(elements.get("result"))
        result = elements.get("result")
        self.assertIsNotNone(result.get("totalCount"))
        self.assertEqual(result["totalCount"], 2)
        self.assertIsNotNone(result.get("page"))
        self.assertEqual(result["page"], 1)
        self.assertIsNotNone(result.get("perPage"))
        self.assertEqual(result["perPage"], 100)
