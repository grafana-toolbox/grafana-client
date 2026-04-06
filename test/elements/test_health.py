import sys
import unittest

import pytest
from verlib2 import Version

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class HealthTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api):
        self.grafana = grafana_api

    def test_healthcheck(self):
        """Assume Grafana 6 or higher"""
        result = self.grafana.health.check()
        self.assertGreater(Version(result["version"]), Version("6"))
