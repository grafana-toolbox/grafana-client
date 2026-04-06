import sys
import typing as t
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
)

params = dict(
    time_from=1563183710618,
    time_to=1563185212275,
    # alert_id=11,  # noqa: ERA001
    # dashboard_id=111,  # noqa: ERA001
    # panel_id=22,  # noqa: ERA001
    user_id=1,
    ann_type="annotation",
    tags=["tags-test"],
    limit=1,
)

pytestmark = pytest.mark.integration


@pytest.fixture()
def annotation_id(annotation_provisioned) -> str:
    return annotation_provisioned["id"]


@pytest.fixture()
def annotation_provisioned(grafana_api, dashboard_uid) -> t.Dict:

    # Prune all annotations.
    for annotation in grafana_api.annotations.find_annotations():
        grafana_api.annotations.delete_annotations_by_id(annotation["id"])

    # Provision annotation.
    return grafana_api.annotations.add_annotation(
        dashboard_uid=dashboard_uid,
        tags=["tags-test"],
        text="Annotation Description",
        time_from=1563183710618,
        time_to=1563185212275,
    )


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class AnnotationsTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(self, grafana_api: GrafanaApi, dashboard_uid: str, dashboard_id: str, annotation_id: str):
        self.grafana = grafana_api
        self.dashboard_id = dashboard_id
        self.dashboard_uid = dashboard_uid
        self.annotation_id = annotation_id

    def test_find_all(self):
        annotations = self.grafana.annotations.find_annotations()
        self.assertEqual(len(annotations), 1, "Wrong number of annotations")
        self.assertEqual(annotations[0]["text"], "Annotation Description")
        self.assertEqual(annotations[0]["tags"], ["tags-test"])
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(annotations[0]["dashboardUID"], self.dashboard_uid)

    def test_find_by_dashboard_uid(self):
        annotations = self.grafana.annotations.find_annotations(
            dashboard_uid=self.dashboard_uid,
        )
        self.assertEqual(len(annotations), 1, "Wrong number of annotations")

    def test_delete_annotation_by_id_success(self):
        response = self.grafana.annotations.delete_annotations_by_id(annotations_id=self.annotation_id)
        self.assertEqual(response["message"], "Annotation deleted")

    def test_delete_annotation_by_id_not_exists(self):
        # FIXME: Grafana 11 & 12 do not care about the outcome of an annotation delete request,
        #        i.e. don't raise an exception when deleting invalid annotations?
        if Version(self.grafana.version) >= Version("11"):
            response = self.grafana.annotations.delete_annotations_by_id(annotations_id=9999)
            self.assertEqual(response["message"], "Annotation deleted")
        else:
            with self.assertRaises((GrafanaClientError, GrafanaServerError)) as excinfo:
                self.grafana.annotations.delete_annotations_by_id(annotations_id=9999)
            self.assertRegex(excinfo.exception.message, "(Annotation not found|Could not find annotation to update)")

    def test_delete_annotation_by_id_null(self):
        if Version(self.grafana.version) >= Version("8"):
            with self.assertRaises(GrafanaBadInputError) as excinfo:
                self.grafana.annotations.delete_annotations_by_id(annotations_id=None)
            self.assertRegex(excinfo.exception.message, "annotationId is invalid")

        # Grafana 7 does not fail here.
        else:
            self.grafana.annotations.delete_annotations_by_id(annotations_id=None)

    def test_add_annotation_no_text(self):
        with self.assertRaises(GrafanaBadInputError) as excinfo:
            self.grafana.annotations.add_annotation()
        self.assertRegex(excinfo.exception.message, "Failed to save annotation")

    def test_add_annotation_no_dashboard(self):
        response = self.grafana.annotations.add_annotation(text="Test")
        self.assertEqual(response["message"], "Annotation added")

    def test_add_annotation_with_dashboard_id(self):
        response = self.grafana.annotations.add_annotation(
            dashboard_id=self.dashboard_id,
            text="42",
        )
        self.assertEqual(response["message"], "Annotation added")

    def test_add_annotation_with_dashboard_uid(self):
        response = self.grafana.annotations.add_annotation(
            dashboard_uid=self.dashboard_uid,
            text="42",
        )
        self.assertEqual(response["message"], "Annotation added")

    def test_add_annotation_graphite(self):
        response = self.grafana.annotations.add_annotation_graphite(
            what="Event - deploy", tags=["deploy", "production"], when=1467844481, data="Data"
        )
        self.assertEqual(response["message"], "Graphite annotation added")

    def test_update_annotation_full(self):
        response = self.grafana.annotations.update_annotation(
            annotations_id=self.annotation_id,
            time_from=1563183710618,
            time_to=1563185212275,
            tags=["tags-test"],
            text="Test",
        )
        self.assertEqual(response["message"], "Annotation updated")

    def test_update_annotation_partial(self):
        grafana9 = Version("9") <= Version(self.grafana.version) < Version("10")
        if grafana9:
            pytest.skip("Updating annotation partially hangs indefinitely on Grafana 9?")
        response = self.grafana.annotations.partial_update_annotation(
            annotations_id=self.annotation_id, tags=["tag1", "tag2"], text="Test"
        )
        self.assertEqual(response["message"], "Annotation patched")


@pytest.mark.parametrize("parameter", params.keys())
def test_find_by_param(grafana_api, annotation_id: str, parameter: str):  # noqa: ARG001
    """
    Invoke "find annotations" operation per parameter.
    """
    kwargs = {parameter: params[parameter]}
    annotations = grafana_api.annotations.find_annotations(**kwargs)
    assert len(annotations) == 1, "Wrong number of annotations"
