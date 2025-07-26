import unittest

import requests
import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError, GrafanaClientError


class LibraryElementTestCase(unittest.TestCase):
    ConnectedPanelJSON: dict = {
        "id": 2,
        "kind": 1,
        "meta": {"connectedDashboards": 2, "folderName": "Pulsar", "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a"},
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
        "uid": "cec85d6f-834b-427e-8993-562d34fff5c4",
        "version": 1,
    }
    ConnectedPanelUID: str = "cec85d6f-834b-427e-8993-562d34fff5c4"
    ConnectedPanelName: str = "CPU Seconds"
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
    ConnectedPanelConnectionUIDs: list = (
        "de3791ac-6079-4c18-bde0-cb390c079722",
        "a45fbfd0-b211-45fc-96ae-a56886075948",
    )
    UnconnectedPanelJSON: dict = {
        "id": 3,
        "kind": 1,
        "meta": {
            "folderName": "Pulsar",
            "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
        },
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
    UnconnectedPanelUID: str = "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6"
    UnconnectedPanelName: str = "Heap Memory"
    UnconnectedPanelConnectionsJSON: dict = {"result": []}
    MissingPanelUID: str = "missing-panel"
    MissingPanelName: str = "Unknown name"

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
    CreatePanelUID: str = "cec85d6f-834b-427e-8993-562d34fff5c4"
    CreatePanelName: str = "CPU Seconds"
    CreatePanelFolderUID: str = "d6818acd-f7b1-433e-a679-7f206a7ce37a"
    CreatePanelResponseJSON: dict = {
        "result": {
            "id": 4,
            "orgId": 1,
            "folderId": 100,
            "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
            "uid": "cec85d6f-834b-427e-8993-562d34fff5c4",
            "name": "CPU Seconds",
            "kind": 1,
            "type": "timeseries",
            "description": "",
            "model": {
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
            },
            "version": 1,
            "meta": {
                "folderName": "Pulsar",
                "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                "connectedDashboards": 0,
                "created": "2024-02-06T14:47:17.635073-06:00",
                "updated": "2024-02-06T14:47:17.635073-06:00",
                "createdBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
                "updatedBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
            },
        }
    }
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
    UpdatePanelResponseJSON: dict = {
        "result": {
            "id": 4,
            "orgId": 1,
            "folderId": 100,
            "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
            "uid": "cec85d6f-834b-427e-8993-562d34fff5c4",
            "name": "CPU Seconds",
            "kind": 1,
            "type": "timeseries",
            "description": "",
            "model": {
                "datasource": {"type": "prometheus", "uid": "d2caab40-4055-4236-a9b3-67ae334e096c"},
                "description": "",
                "gridPos": {"h": 8, "w": 12, "x": 10, "y": 15},
                "id": 2,
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
            "version": 2,
            "meta": {
                "folderName": "Pulsar",
                "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                "connectedDashboards": 0,
                "created": "2024-02-06T14:47:17-06:00",
                "updated": "2024-02-06T16:45:47.503116-06:00",
                "createdBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
                "updatedBy": {"avatarUrl": "/avatar/46d229b033af06a191ff2267bca9ae56", "id": 1, "name": "admin"},
            },
        }
    }
    UpdatePanelUID: str = "cec85d6f-834b-427e-8993-562d34fff5c4"
    UpdatePanelName: str = "CPU Seconds"
    UpdatePanelFolderUID: str = "d6818acd-f7b1-433e-a679-7f206a7ce37a"
    ListLibraryElementsResponseJSON: dict = {
        "result": {
            "totalCount": 2,
            "elements": [
                {
                    "id": 5,
                    "orgId": 1,
                    "folderId": 100,
                    "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                    "uid": "cec85d6f-834b-427e-8993-562d34fff5c4",
                    "name": "CPU Seconds",
                    "kind": 1,
                    "type": "timeseries",
                    "description": "",
                    "model": {
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
                        "id": 1,
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
                                "expr": 'rate(process_cpu_seconds_total{job=~"$Job", instance=~"$Instance"}[$__rate_interval])',  # noqa: E501
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
                    },
                    "version": 1,
                    "meta": {
                        "folderName": "Pulsar",
                        "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                        "connectedDashboards": 0,
                        "created": "2024-02-07T10:25:19-06:00",
                        "updated": "2024-02-07T10:25:19-06:00",
                        "createdBy": {
                            "avatarUrl": "/avatar/3dbccb5e89c37491dae50c6a4be200c6",
                            "id": 2,
                            "name": "sa-tibco-messaging-monitoring",
                        },
                        "updatedBy": {
                            "avatarUrl": "/avatar/3dbccb5e89c37491dae50c6a4be200c6",
                            "id": 2,
                            "name": "sa-tibco-messaging-monitoring",
                        },
                    },
                },
                {
                    "id": 6,
                    "orgId": 1,
                    "folderId": 100,
                    "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                    "uid": "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6",
                    "name": "Heap Memory",
                    "kind": 1,
                    "type": "timeseries",
                    "description": "",
                    "model": {
                        "datasource": {"type": "prometheus", "uid": "fb5e0357-258c-4831-b447-565be35828b5"},
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
                                    "fillOpacity": 10,
                                    "gradientMode": "none",
                                    "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                                    "insertNulls": False,
                                    "lineInterpolation": "linear",
                                    "lineWidth": 1,
                                    "pointSize": 5,
                                    "scaleDistribution": {"type": "linear"},
                                    "showPoints": "never",
                                    "spanNulls": False,
                                    "stacking": {"group": "A", "mode": "none"},
                                    "thresholdsStyle": {"mode": "off"},
                                },
                                "mappings": [],
                                "min": 0,
                                "thresholds": {
                                    "mode": "absolute",
                                    "steps": [{"color": "green", "value": None}, {"color": "red", "value": 80}],
                                },
                                "unit": "decbytes",
                            },
                            "overrides": [],
                        },
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                        "id": 3,
                        "interval": "1m",
                        "libraryPanel": {"name": "Heap Memory", "uid": "b07d36c0-b5f6-4228-b0c0-d3c21e16a5f6"},
                        "links": [],
                        "options": {
                            "legend": {
                                "calcs": ["lastNotNull"],
                                "displayMode": "list",
                                "placement": "bottom",
                                "showLegend": False,
                            },
                            "tooltip": {"mode": "multi", "sort": "none"},
                        },
                        "pluginVersion": "10.2.2",
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
                        "transparent": True,
                        "type": "timeseries",
                    },
                    "version": 1,
                    "meta": {
                        "folderName": "Pulsar",
                        "folderUid": "d6818acd-f7b1-433e-a679-7f206a7ce37a",
                        "connectedDashboards": 0,
                        "created": "2024-02-07T10:25:37-06:00",
                        "updated": "2024-02-07T10:25:37-06:00",
                        "createdBy": {
                            "avatarUrl": "/avatar/3dbccb5e89c37491dae50c6a4be200c6",
                            "id": 2,
                            "name": "sa-tibco-messaging-monitoring",
                        },
                        "updatedBy": {
                            "avatarUrl": "/avatar/3dbccb5e89c37491dae50c6a4be200c6",
                            "id": 2,
                            "name": "sa-tibco-messaging-monitoring",
                        },
                    },
                },
            ],
            "page": 1,
            "perPage": 100,
        }
    }

    HealthResponsePre8_2: dict = {"buildInfo": {"commit": "unknown", "version": "8.1.8"}}
    HealthResponsePost8_2: dict = {"buildInfo": {"commit": "unknown-dev", "version": "10.2.2"}}

    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_library_element(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.ConnectedPanelUID}",
            json=LibraryElementTestCase.ConnectedPanelJSON,
        )
        element = self.grafana.libraryelement.get_library_element(LibraryElementTestCase.ConnectedPanelUID)
        self.assertEqual(element["uid"], LibraryElementTestCase.ConnectedPanelUID)

    @requests_mock.Mocker()
    def test_get_library_element_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.ConnectedPanelUID}",
            json=LibraryElementTestCase.ConnectedPanelJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element(LibraryElementTestCase.ConnectedPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_notfound(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.MissingPanelUID}",
            json={"message": "library element could not be found"},
            status_code=404,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @requests_mock.Mocker()
    def test_get_library_element_notfound_grafana_pre_8_2(self, m):
        def custom_matcher(request):
            if request.path_url == "/api/frontend/settings":
                return None
            resp = requests.Response()
            resp.status_code = 404
            resp._content = b'{"message": "library element could not be found"}'
            resp.headers["Content-Type"] = "application/json"
            return resp

        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.add_matcher(custom_matcher)
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_by_name(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/name/{LibraryElementTestCase.ConnectedPanelName}",
            json=LibraryElementTestCase.ConnectedPanelJSON,
        )
        element = self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.ConnectedPanelName)
        self.assertEqual(element["name"], LibraryElementTestCase.ConnectedPanelName)

    @requests_mock.Mocker()
    def test_get_library_element_by_name_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/name/{LibraryElementTestCase.ConnectedPanelName}",
            json=LibraryElementTestCase.ConnectedPanelJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.ConnectedPanelName)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_by_name_notfound(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/name/{LibraryElementTestCase.MissingPanelName}",
            json={"message": "library element could not be found"},
            status_code=404,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.MissingPanelName)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @requests_mock.Mocker()
    def test_get_library_element_by_name_notfound_grafana_pre_8_2(self, m):
        def custom_matcher(request):
            if request.path_url == "/api/frontend/settings":
                return None
            resp = requests.Response()
            resp.status_code = 404
            resp._content = b'{"message": "library element could not be found"}'
            resp.headers["Content-Type"] = "application/json"
            return resp

        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.add_matcher(custom_matcher)
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element_by_name(LibraryElementTestCase.MissingPanelName)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_connections(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.ConnectedPanelUID}/connections",
            json=LibraryElementTestCase.ConnectedPanelConnectionsJSON,
        )
        connections = self.grafana.libraryelement.get_library_element_connections(
            LibraryElementTestCase.ConnectedPanelUID
        )
        self.assertEqual(len(connections["result"]), 2)
        self.assertIn(connections["result"][0]["connectionUid"], LibraryElementTestCase.ConnectedPanelConnectionUIDs)
        self.assertIn(connections["result"][1]["connectionUid"], LibraryElementTestCase.ConnectedPanelConnectionUIDs)

    @requests_mock.Mocker()
    def test_get_library_element_connections_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.ConnectedPanelUID}/connections",
            json=LibraryElementTestCase.ConnectedPanelConnectionsJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element_connections(LibraryElementTestCase.ConnectedPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_connections_notfound(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.MissingPanelUID}/connections",
            json={"message": "library element could not be found"},
            status_code=404,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.get_library_element_connections(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @requests_mock.Mocker()
    def test_get_library_element_connections_notfound_grafana_pre_8_2(self, m):
        def custom_matcher(request):
            if request.path_url == "/api/frontend/settings":
                return None
            resp = requests.Response()
            resp.status_code = 404
            resp._content = b'{"message": "library element could not be found"}'
            resp.headers["Content-Type"] = "application/json"
            return resp

        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.add_matcher(custom_matcher)
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_get_library_element_connections_noconnections(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.UnconnectedPanelUID}/connections",
            json=LibraryElementTestCase.UnconnectedPanelConnectionsJSON,
        )
        connections = self.grafana.libraryelement.get_library_element_connections(
            LibraryElementTestCase.UnconnectedPanelUID
        )
        self.assertEqual(len(connections["result"]), 0)

    @requests_mock.Mocker()
    def test_get_library_element_connections_noconnections_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.get(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.UnconnectedPanelUID}/connections",
            json=LibraryElementTestCase.UnconnectedPanelConnectionsJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.get_library_element_connections(LibraryElementTestCase.UnconnectedPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_create_library_element(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.post(
            "http://localhost/api/library-elements",
            json=LibraryElementTestCase.CreatePanelResponseJSON,
        )
        resp = self.grafana.libraryelement.create_library_element(
            model=LibraryElementTestCase.CreatePanelModelJSON,
            name=LibraryElementTestCase.CreatePanelName,
            uid=LibraryElementTestCase.CreatePanelUID,
            folder_uid=LibraryElementTestCase.CreatePanelFolderUID,
        )
        self.assertIsNotNone(resp["result"])
        self.assertIsNotNone(resp["result"]["folderUid"])
        self.assertEqual(resp["result"]["folderUid"], LibraryElementTestCase.CreatePanelFolderUID)
        self.assertIsNotNone(resp["result"]["uid"])
        self.assertEqual(resp["result"]["uid"], LibraryElementTestCase.CreatePanelUID)
        self.assertIsNotNone(resp["result"]["model"])

    @requests_mock.Mocker()
    def test_create_library_element_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.post(
            "http://localhost/api/library-elements",
            json=LibraryElementTestCase.CreatePanelResponseJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.create_library_element(
                model=LibraryElementTestCase.CreatePanelModelJSON,
                name=LibraryElementTestCase.CreatePanelName,
                uid=LibraryElementTestCase.CreatePanelUID,
                folder_uid=LibraryElementTestCase.CreatePanelFolderUID,
            )
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_create_library_element_already_exists(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.post(
            "http://localhost/api/library-elements",
            json={"message": "library element with that name or UID already exists"},
            status_code=400,
        )
        with self.assertRaisesRegex(
            GrafanaBadInputError, "Bad Input: .*library element with that name or UID already exists.*"
        ):
            self.grafana.libraryelement.create_library_element(
                model=LibraryElementTestCase.CreatePanelModelJSON,
                name=LibraryElementTestCase.CreatePanelName,
                uid=LibraryElementTestCase.CreatePanelUID,
                folder_uid=LibraryElementTestCase.CreatePanelFolderUID,
            )

    @requests_mock.Mocker()
    def test_update_library_element(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.patch(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.UpdatePanelUID}",
            json=LibraryElementTestCase.UpdatePanelResponseJSON,
        )
        resp = self.grafana.libraryelement.update_library_element(
            model=LibraryElementTestCase.UpdatePanelModelJSON,
            name=LibraryElementTestCase.UpdatePanelName,
            uid=LibraryElementTestCase.UpdatePanelUID,
            folder_uid=LibraryElementTestCase.UpdatePanelFolderUID,
            version=1,
        )
        self.assertIsNotNone(resp["result"])
        self.assertIsNotNone(resp["result"]["folderUid"])
        self.assertEqual(resp["result"]["folderUid"], LibraryElementTestCase.CreatePanelFolderUID)
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

    @requests_mock.Mocker()
    def test_update_library_element_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.patch(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.UpdatePanelUID}",
            json=LibraryElementTestCase.UpdatePanelResponseJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.update_library_element(
                model=LibraryElementTestCase.UpdatePanelModelJSON,
                name=LibraryElementTestCase.UpdatePanelName,
                uid=LibraryElementTestCase.UpdatePanelUID,
                folder_uid=LibraryElementTestCase.UpdatePanelFolderUID,
                version=1,
            )
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_update_library_element_notfound(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.patch(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.MissingPanelUID}",
            json={"message": "library element could not be found"},
            status_code=404,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.update_library_element(
                model=LibraryElementTestCase.UpdatePanelModelJSON,
                name=LibraryElementTestCase.UpdatePanelName,
                uid=LibraryElementTestCase.MissingPanelUID,
                folder_uid=LibraryElementTestCase.UpdatePanelFolderUID,
                version=1,
            )
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @requests_mock.Mocker()
    def test_delete_library_element_connections(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.delete(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.ConnectedPanelUID}",
            json={"message": "the library element has connections"},
            status_code=403,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.ConnectedPanelUID)
        self.assertEqual(403, ex.exception.status_code)
        self.assertEqual("Client Error 403: the library element has connections", ex.exception.message)

    @requests_mock.Mocker()
    def test_delete_library_element_noconnections(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.delete(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.UnconnectedPanelUID}",
            json={"id": 4, "message": "Library element deleted"},
        )
        resp = self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.UnconnectedPanelUID)
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp.get("message"))
        self.assertEqual("Library element deleted", resp.get("message"))

    @requests_mock.Mocker()
    def test_delete_library_element_notfound(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.delete(
            f"http://localhost/api/library-elements/{LibraryElementTestCase.MissingPanelUID}",
            json={"message": "library element could not be found"},
            status_code=404,
        )
        with self.assertRaises(GrafanaClientError) as ex:
            self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(404, ex.exception.status_code)
        self.assertEqual("Client Error 404: library element could not be found", ex.exception.message)

    @requests_mock.Mocker()
    def test_delete_library_element_notfound_grafana_pre_8_2(self, m):
        def custom_matcher(request):
            if request.path_url == "/api/frontend/settings":
                return None
            resp = requests.Response()
            resp.status_code = 404
            resp._content = b'{"message": "library element could not be found"}'
            resp.headers["Content-Type"] = "application/json"
            return resp

        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.add_matcher(custom_matcher)
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.delete_library_element(LibraryElementTestCase.MissingPanelUID)
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )

    @requests_mock.Mocker()
    def test_list_library_elements(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePost8_2,
        )
        m.get(
            "http://localhost/api/library-elements?",
            json=LibraryElementTestCase.ListLibraryElementsResponseJSON,
        )
        elements = self.grafana.libraryelement.list_library_elements()
        self.assertIsNotNone(elements.get("result"))
        result = elements.get("result")
        self.assertIsNotNone(result.get("totalCount"))
        self.assertEqual(result["totalCount"], 2)
        self.assertIsNotNone(result.get("page"))
        self.assertEqual(result["page"], 1)
        self.assertIsNotNone(result.get("perPage"))
        self.assertEqual(result["perPage"], 100)

    @requests_mock.Mocker()
    def test_list_library_elements_grafana_pre_8_2(self, m):
        m.get(
            "http://localhost/api/frontend/settings",
            json=LibraryElementTestCase.HealthResponsePre8_2,
        )
        m.get(
            "http://localhost/api/library-elements?",
            json=LibraryElementTestCase.ListLibraryElementsResponseJSON,
        )
        with self.assertRaises(DeprecationWarning) as ex:
            self.grafana.libraryelement.list_library_elements()
        self.assertEqual(
            "Grafana versions earlier than 8.2 do not support library elements",
            str(ex.exception),
        )
