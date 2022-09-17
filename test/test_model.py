import unittest

from grafana_client.model import DatasourceHealthResponse

dhr = DatasourceHealthResponse(
    uid="uid",
    type="type",
    success=True,
    status="status",
    message="message",
    duration=42.42,
    response={},
)


class ModelTestCase(unittest.TestCase):
    def test_datasource_health_response_asdict(self):
        data = dhr.asdict()
        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) > 1)
        self.assertIn("response", data)

    def test_datasource_health_response_asdict_compact(self):
        data = dhr.asdict_compact()
        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) > 1)
        self.assertNotIn("response", data)
