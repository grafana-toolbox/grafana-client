import logging
import unittest

from grafana_client.util import as_bool, setup_logging


class UtilTestCase(unittest.TestCase):
    def test_setup_logging(self):
        setup_logging(level=logging.WARNING)

    def test_as_bool_success(self):
        self.assertTrue(as_bool("true"))
        self.assertFalse(as_bool("false"))
        self.assertFalse(as_bool(None))

    def test_as_bool_failure(self):
        self.assertRaises(ValueError, lambda: as_bool("foo"))
