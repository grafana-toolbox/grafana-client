import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class ServiceAccountsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi, reset_user_model):  # noqa: ARG002
        self.grafana = grafana_api
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Service accounts only supported by Grafana 9 and higher.")
        self.account = self.grafana.serviceaccount.create({"name": "service", "role": "Admin"})
        self.account_id = self.account["id"]
        self.token = self.grafana.serviceaccount.create_token(self.account_id, {"name": "some-uuid"})
        self.token_id = self.token["id"]
        if Version(self.grafana.version) >= Version("11"):
            self.account_uid = self.account["uid"]

    def test_get_account(self):
        result = self.grafana.serviceaccount.get(self.account_id)
        self.assertEqual(self.account_id, result["id"])
        self.assertEqual("service", result["name"])
        if Version(self.grafana.version) >= Version("10.4"):
            self.assertEqual("sa-1-service", result["login"])
        else:
            self.assertEqual("sa-service", result["login"])
        self.assertEqual("Admin", result["role"])
        self.assertEqual(1, result["orgId"])
        self.assertEqual(False, result["isDisabled"])
        self.assertEqual(
            {
                "serviceaccounts.permissions:read": True,
                "serviceaccounts.permissions:write": True,
                "serviceaccounts:delete": True,
                "serviceaccounts:read": True,
                "serviceaccounts:write": True,
            },
            result["accessControl"],
        )

    def test_create_account(self):
        user = self.grafana.serviceaccount.create({"name": "foo", "role": "Admin"})
        user_login = user["login"]
        self.assertTrue(user_login.startswith("sa-"), f"Expected login to start with 'sa-', got {user_login}")

    def test_update_account(self):
        response = self.grafana.serviceaccount.update(self.account_id, {"name": "foo", "role": "Admin"})
        self.assertEqual(response["message"], "Service account updated")

    def test_delete_account(self):
        response = self.grafana.serviceaccount.delete(self.account_id)
        self.assertEqual(response["message"], "Service account deleted")

    def test_create_token_success(self):
        token = self.grafana.serviceaccount.create_token(self.account_id, {"name": "random-token"})
        self.assertEqual(token["name"], "random-token")

    def test_create_token_duplicate(self):
        with self.assertRaises(GrafanaBadInputError) as context:
            self.grafana.serviceaccount.create_token(self.account_id, {"name": "some-uuid"})
        self.assertEqual(400, context.exception.status_code)
        self.assertIn(
            "service account token with given name already exists in the organization", context.exception.message
        )

    def test_delete_token(self):
        response = self.grafana.serviceaccount.delete_token(self.account_id, self.token_id)
        self.assertEqual(response["message"], "Service account token deleted")

    def test_get_tokens_success(self):
        results = self.grafana.serviceaccount.get_tokens(self.account_id)
        self.assertEqual(1, len(results))

    def test_get_tokens_no_results(self):
        results = self.grafana.serviceaccount.get_tokens(9999)
        self.assertEqual(0, len(results))

    def test_search_success(self):
        results = self.grafana.serviceaccount.search_all("serv")
        self.assertEqual(1, len(results))
        self.assertEqual("service", results[0]["name"])

    def test_search_paged_too_far(self):
        results = self.grafana.serviceaccount.search_all("serv", page=9999)
        self.assertEqual(0, len(results))

    def test_search_paged_too_short(self):
        results = self.grafana.serviceaccount.search_all("serv", page=0)
        self.assertEqual(1, len(results))

    def test_search_paged_invalid(self):
        results = self.grafana.serviceaccount.search_all("serv", page=-9999)
        self.assertEqual(1, len(results))

    def test_search_one_success(self):
        result = self.grafana.serviceaccount.search_one("serv")
        self.assertEqual("service", result["name"])

    def test_search_one_find_two(self):
        self.grafana.serviceaccount.create({"name": "service-2", "role": "Admin"})
        with self.assertRaises(ValueError) as ex:
            self.grafana.serviceaccount.search_one("serv")
        self.assertEqual("More than one service account matched", str(ex.exception))

    def test_search_one_find_zero(self):
        with self.assertRaises(ValueError) as ex:
            self.grafana.serviceaccount.search_one("foo")
        self.assertEqual("No service account matched", str(ex.exception))
