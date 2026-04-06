import sys
import unittest

import pytest
from verlib2 import Version

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError, GrafanaClientError

pytestmark = pytest.mark.integration


@unittest.skipIf("unittest" in sys.argv[0], "Skipping unittest, please use pytest")
class FolderTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def use_fixtures(
        self,
        grafana_api: GrafanaApi,
        dashboard_folder_permissions,
        folder_id: str,
        folder_uid: str,
        folder_title: str,
        user_id: int,
    ):
        self.grafana = grafana_api
        self.folder_id = folder_id
        self.folder_uid = folder_uid
        self.folder_title = folder_title
        self.user_id = user_id
        self.permissions = dashboard_folder_permissions

    def test_get_all_folders(self):
        folders = self.grafana.folder.get_all_folders()
        self.assertEqual(len(folders), 1, "Wrong number of folders")
        self.assertEqual(folders[0]["uid"], self.folder_uid)

    def test_get_folder_by_id(self):
        folder_id = self.folder_id
        folder = self.grafana.folder.get_folder_by_id(folder_id=folder_id)
        self.assertEqual(folder["id"], folder_id)

    def test_get_folder_by_uid(self):
        folder = self.grafana.folder.get_folder(uid=self.folder_uid)
        self.assertEqual(folder["title"], "Testdrive")

    def test_subfolders(self):
        subfolder_uid = "nErXDvCkzz"

        folder = self.grafana.folder.create_folder(
            title="Subdepartment ABC", uid=subfolder_uid, parent_uid=self.folder_uid
        )
        self.assertEqual(folder["uid"], subfolder_uid)
        # 'parentUid' only returned for folders by Grafana 11 and higher.
        if Version(self.grafana.version) >= Version("11"):
            self.assertEqual(folder["parentUid"], self.folder_uid)

        # Grafana 11 and higher only returns top-level folders, or is the outcome just flaky?
        folders = self.grafana.folder.get_all_folders()
        self.assertGreaterEqual(len(folders), 1, "Wrong number of folders")

    def test_create_folder_empty_title(self):
        with self.assertRaises(GrafanaBadInputError) as excinfo:
            self.grafana.folder.create_folder(title=None)
        self.assertEqual(excinfo.exception.status_code, 400)
        self.assertRegex(excinfo.exception.message, "folder title cannot be empty")

    def test_move_folder(self):
        """
        Validate folder move operation on Grafana 11 and higher.

        Grafana 10: Client Error 404: To use this service, you need to activate nested folder feature.
        """
        if Version(self.grafana.version) < Version("11"):
            pytest.skip("Moving folders supported by Grafana 11 and higher.")
        container = self.grafana.folder.create_folder("container")
        container_uid = container["uid"]
        folder = self.grafana.folder.move_folder(uid=self.folder_uid, parent_uid=container_uid)
        self.assertEqual(folder["uid"], self.folder_uid)
        self.assertEqual(folder["parentUid"], container_uid)

    def test_update_folder_title(self):
        folder = self.grafana.folder.update_folder(title="Departmenet DEF", uid=self.folder_uid, overwrite=True)
        self.assertEqual(folder["title"], "Departmenet DEF")
        self.assertEqual(folder["uid"], self.folder_uid)

    def test_update_folder_uid(self):
        if Version(self.grafana.version) >= Version("10"):
            pytest.skip("Updating a folder uid only supported up to Grafana 10.")

        new_folder_uid = "oFsYEwDlaa"
        new_title = self.folder_title
        folder = self.grafana.folder.update_folder(
            title=new_title, uid=self.folder_uid, new_uid=new_folder_uid, overwrite=True
        )
        self.assertEqual(folder["uid"], new_folder_uid)

    def test_update_folder_conflict(self):
        with self.assertRaises(GrafanaClientError) as excinfo:
            self.grafana.folder.update_folder(title="Departmenet DEF", uid=self.folder_uid)
        self.assertEqual(excinfo.exception.status_code, 412)
        self.assertRegex(
            excinfo.exception.message, "Client Error 412: [Tt]he (folder|dashboard) has been changed by someone else"
        )

    def test_get_folder_permissions(self):
        folder_permissions = self.grafana.folder.get_folder_permissions(uid=self.folder_uid)
        if Version(self.grafana.version) >= Version("9"):
            self.assertEqual(folder_permissions[0]["permissionName"], "Admin")
        else:
            self.assertEqual(folder_permissions[0]["permissionName"], "View")

    def test_update_folder_permissions_standard(self):
        folder = self.grafana.folder.update_folder_permissions(
            uid=self.folder_uid,
            items=self.permissions,
        )
        self.assertRegex(folder["message"], "(Folder|Dashboard) permissions updated")

    def test_update_folder_permissions_for_user(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Updating folder permissions for users supported by Grafana 9 and higher.")
        folder = self.grafana.folder.update_folder_permissions_for_user(
            uid=self.folder_uid,
            user_id=self.user_id,
            items=self.permissions,
        )
        self.assertEqual(folder["message"], "Permission removed")

    def test_update_folder_permissions_unknown_user(self):
        if Version(self.grafana.version) < Version("9"):
            pytest.skip("Updating folder permissions for users supported by Grafana 9 and higher.")
        with self.assertRaises(GrafanaBadInputError) as excinfo:
            self.grafana.folder.update_folder_permissions_for_user(
                uid=self.folder_uid,
                user_id="12345",
                items=self.permissions,
            )
        if Version(self.grafana.version) >= Version("11"):
            self.assertRegex(excinfo.exception.message, "user not found")
        else:
            self.assertRegex(excinfo.exception.message, "failed to set user permission")

    def test_delete_folder(self):
        folder = self.grafana.folder.delete_folder(uid=self.folder_uid)
        version9 = Version("9") <= Version(self.grafana.version) < Version("10")
        if not version9:
            self.assertRegex(folder["message"], "Folder.+deleted")
