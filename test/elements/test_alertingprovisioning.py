import unittest

from test.elements.test_alertingprovisioning_fixtures import (
    ALERTRULE,
)

import requests_mock

from grafana_client import GrafanaApi


class AlertingProvisioningTestCase(unittest.TestCase):
  def setUp(self):
      self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

  @requests_mock.Mocker()
  def test_get_alertrule(self, m):
      m.get(
          "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
          json=ALERTRULE
      )
      response = self.grafana.alertingprovisioning.get_alertrule("bUUGqLiVk")
      self.assertEqual(response["uid"], "bUUGqLiVk")

  @requests_mock.Mocker()
  def test_delete_alertrule(self, m):
      m.delete("http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk", json={"uid": "bUUGqLiVk"})
      response = self.grafana.alertingprovisioning.delete_alertrule("bUUGqLiVk")
      self.assertEqual(response["uid"], "bUUGqLiVk")

  @requests_mock.Mocker()
  def test_create_alertrule(self, m):
      m.post(
          "http://localhost/api/v1/provisioning/alert-rules",
          json=ALERTRULE,
      )

      response = self.grafana.alertingprovisioning.create_alertrule(ALERTRULE)
      self.assertEqual(response["uid"], "bUUGqLiVk")
  
  @requests_mock.Mocker()
  def test_update_alertrule(self, m):
      m.put(
          "http://localhost/api/v1/provisioning/alert-rules/bUUGqLiVk",
          json=ALERTRULE,
      )

      response = self.grafana.alertingprovisioning.update_alertrule(alertrule_uid="bUUGqLiVk",alertrule=ALERTRULE)
      self.assertEqual(response["uid"], "bUUGqLiVk")
      