import unittest

import requests_mock

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaBadInputError


class FolderTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_get_all_folders(self, m):
        m.get(
            "http://localhost/api/folders",
            json=[
                {
                    "id": 1,
                    "uid": "nErXDvCkzz",
                    "title": "Departmenet ABC",
                    "url": "/dashboards/f/nErXDvCkzz/department-abc",
                    "hasAcl": "false",
                    "canSave": "false",
                    "canEdit": "false",
                    "canAdmin": "false",
                    "createdBy": "admin",
                    "created": "2018-01-31T17:43:12+01:00",
                    "updatedBy": "admin",
                    "updated": "2018-01-31T17:43:12+01:00",
                    "version": 1,
                }
            ],
        )
        folders = self.grafana.folder.get_all_folders()
        self.assertEqual(folders[0]["id"], 1)
        self.assertEqual(len(folders), 1)

    @requests_mock.Mocker()
    def test_get_folder(self, m):
        m.get(
            "http://localhost/api/folders/nErXDvCkzzh",
            json={
                "id": 1,
                "uid": "nErXDvCkzzh",
                "title": "Departmenet ABC",
                "url": "/dashboards/f/nErXDvCkzz/department-abc",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folders = self.grafana.folder.get_folder(uid="nErXDvCkzzh")
        self.assertEqual(folders["uid"], "nErXDvCkzzh")

    @requests_mock.Mocker()
    def test_create_folder(self, m):
        m.post(
            "http://localhost/api/folders",
            json={
                "id": 1,
                "uid": "nErXDvCkzz",
                "title": "Departmenet ABC",
                "url": "/dashboards/f/nErXDvCkzz/department-abc",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folder = self.grafana.folder.create_folder(title="Departmenet ABC", uid="nErXDvCkzz")
        self.assertEqual(folder["uid"], "nErXDvCkzz")

    @requests_mock.Mocker()
    def test_create_folder_empty_uid(self, m):
        m.post("http://localhost/api/folders", json={"message": "Folder title cannot be empty"}, status_code=400)
        with self.assertRaises(GrafanaBadInputError):
            self.grafana.folder.create_folder(title="Departmenet ABC")

    @requests_mock.Mocker()
    def test_update_folder(self, m):
        m.put(
            "http://localhost/api/folders/nErXDvCkzz",
            json={
                "id": 1,
                "uid": "nErXDvCkzz",
                "title": "Departmenet DEF",
                "url": "/dashboards/f/nErXDvCkzz/department-def",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folder = self.grafana.folder.update_folder(title="Departmenet DEF", uid="nErXDvCkzz", version=1, overwrite=True)
        self.assertEqual(folder["title"], "Departmenet DEF")
        self.assertEqual(folder["uid"], "nErXDvCkzz")

    @requests_mock.Mocker()
    def test_update_folder_uid(self, m):
        m.put(
            "http://localhost/api/folders/nErXDvCkzz",
            json={
                "id": 1,
                "uid": "oFsYEwDlaa",
                "title": "Departmenet DEF",
                "url": "/dashboards/f/oFsYEwDlaa/department-def",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folder = self.grafana.folder.update_folder(
            title="Departmenet DEF", uid="nErXDvCkzz", new_uid="oFsYEwDlaa", version=1, overwrite=True
        )
        self.assertEqual(folder["title"], "Departmenet DEF")
        self.assertEqual(folder["uid"], "oFsYEwDlaa")

    @requests_mock.Mocker()
    def test_update_folder_some_param(self, m):
        m.put(
            "http://localhost/api/folders/nErXDvCkzz",
            json={
                "id": 1,
                "uid": "nErXDvCkzz",
                "title": "Departmenet DEF",
                "url": "/dashboards/f/nErXDvCkzz/department-def",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folder = self.grafana.folder.update_folder(title="Departmenet DEF", uid="nErXDvCkzz")
        self.assertEqual(folder["title"], "Departmenet DEF")

    @requests_mock.Mocker()
    def test_get_folder_by_id(self, m):
        m.get(
            "http://localhost/api/folders/id/1",
            json={
                "id": 1,
                "uid": "nErXDvCkzz",
                "title": "Departmenet ABC",
                "url": "/dashboards/f/nErXDvCkzz/department-abc",
                "hasAcl": "false",
                "canSave": "false",
                "canEdit": "false",
                "canAdmin": "false",
                "createdBy": "admin",
                "created": "2018-01-31T17:43:12+01:00",
                "updatedBy": "admin",
                "updated": "2018-01-31T17:43:12+01:00",
                "version": 1,
            },
        )
        folder = self.grafana.folder.get_folder_by_id(folder_id=1)
        self.assertEqual(folder["id"], 1)

    @requests_mock.Mocker()
    def test_get_folder_permissions(self, m):
        m.get(
            "http://localhost/api/folders/nErXDvCkzz/permissions",
            json=[
                {
                    "id": 1,
                    "folderId": -1,
                    "created": "2017-06-20T02:00:00+02:00",
                    "updated": "2017-06-20T02:00:00+02:00",
                    "userId": 0,
                    "userLogin": "",
                    "userEmail": "",
                    "teamId": 0,
                    "team": "",
                    "role": "Viewer",
                    "permission": 1,
                    "permissionName": "View",
                    "uid": "nErXDvCkzz",
                    "title": "",
                    "slug": "",
                    "isFolder": "false",
                    "url": "",
                },
                {
                    "id": 2,
                    "dashboardId": -1,
                    "created": "2017-06-20T02:00:00+02:00",
                    "updated": "2017-06-20T02:00:00+02:00",
                    "userId": 0,
                    "userLogin": "",
                    "userEmail": "",
                    "teamId": 0,
                    "team": "",
                    "role": "Editor",
                    "permission": 2,
                    "permissionName": "Edit",
                    "uid": "",
                    "title": "",
                    "slug": "",
                    "isFolder": "false",
                    "url": "",
                },
            ],
        )
        folder_permissions = self.grafana.folder.get_folder_permissions(uid="nErXDvCkzz")
        self.assertEqual(folder_permissions[0]["permissionName"], "View")

    @requests_mock.Mocker()
    def test_update_folder_permissions(self, m):
        m.post("http://localhost/api/folders/nErXDvCkzz/permissions", json={"message": "Folder permissions updated"})
        folder = self.grafana.folder.update_folder_permissions(
            uid="nErXDvCkzz",
            items=[
                {"role": "Viewer", "permission": 1},
                {"role": "Editor", "permission": 2},
                {"teamId": 1, "permission": 1},
                {"userId": 11, "permission": 4},
            ],
        )
        self.assertEqual(folder["message"], "Folder permissions updated")

    @requests_mock.Mocker()
    def test_delete_folder(self, m):
        m.delete("http://localhost/api/folders/nErXDvCkzz", json={"message": "Folder deleted"})
        folder = self.grafana.folder.delete_folder(uid="nErXDvCkzz")
        self.assertEqual(folder["message"], "Folder deleted")
