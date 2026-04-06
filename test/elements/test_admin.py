import sys
import unittest

import pytest
from verlib2 import Version

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class AdminTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api, user_id: int):
        self.grafana = grafana_api
        self.user_id = user_id

    def test_settings(self):
        settings = self.grafana.admin.settings()
        setting_keys = list(settings.keys())
        self.assertIn("server", setting_keys)
        self.assertIn("plugins", setting_keys)
        self.assertIn("security", setting_keys)

    def test_stats(self):
        stats = self.grafana.admin.stats()
        self.assertGreaterEqual(len(stats), 10)

    def test_create_user(self):
        response = self.grafana.admin.create_user(
            {"name": "User", "email": "user@graf.com", "login": "user", "password": "secret"}
        )
        self.assertEqual(response["message"], "User created")

    def test_change_user_password(self):
        response = self.grafana.admin.change_user_password(user_id=self.user_id, password="password")  # noqa: S106
        self.assertEqual(response["message"], "User password updated")

    def test_change_user_permissions(self):
        response = self.grafana.admin.change_user_permissions(user_id=self.user_id, is_grafana_admin=True)
        self.assertEqual(response["message"], "User permissions updated")

    def test_delete_user(self):
        response = self.grafana.admin.delete_user(user_id=self.user_id)
        self.assertEqual(response["message"], "User deleted")

    def test_pause_all_alerts(self):
        if Version(self.grafana.version) >= Version("9"):
            pytest.skip("Legacy alerting was disabled with Grafana 9")
        response = self.grafana.admin.pause_all_alerts(pause=True)
        self.assertEqual(response["message"], "alerts paused")

    def test_enable_user(self):
        response = self.grafana.admin.set_user_enabled(user_id=self.user_id, enabled=True)
        self.assertEqual(response["message"], "User enabled")

    def test_disable_user(self):
        response = self.grafana.admin.set_user_enabled(user_id=self.user_id, enabled=False)
        self.assertEqual(response["message"], "User disabled")
