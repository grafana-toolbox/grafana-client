import sys
import unittest

if sys.version_info < (3, 7, 0):
    raise unittest.SkipTest("Imports will fail on Python 3.6. Skipping all tests in test_package_version.py")

from grafana_client.version import __version__, __version_tuple__


class PackageTestCase(unittest.TestCase):
    def test_package_version(self):
        self.assertIsInstance(__version__, str)
        self.assertGreaterEqual(__version_tuple__, (0, 0, 1))
