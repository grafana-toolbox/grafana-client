import unittest

from grafana_client.version import __version__, __version_tuple__


class PackageTestCase(unittest.TestCase):
    def test_package_version(self):
        self.assertIsInstance(__version__, str)
        self.assertGreaterEqual(__version_tuple__, (3, 0, 0))
