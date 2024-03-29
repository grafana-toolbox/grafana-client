from ..base import Base


class Folder(Base):
    def __init__(self, client):
        super(Folder, self).__init__(client)
        self.client = client

    async def get_all_folders(self):
        """

        :return:
        """
        path = "/folders"
        r = await self.client.GET(path)
        return r

    async def get_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        r = await self.client.GET(path)
        return r

    async def create_folder(self, title, uid=None):
        """

        :param title:
        :param uid:
        :return:
        """
        json_data = dict(title=title)
        if uid is not None:
            json_data["uid"] = uid
        return await self.client.POST("/folders", json=json_data)

    async def update_folder(self, uid, title=None, version=None, overwrite=False, new_uid=None):
        """

        :param uid:
        :param title:
        :param version:
        :param overwrite:
        :param new_uid:
        :return:
        """
        body = {}
        if new_uid:
            body["uid"] = new_uid
        if title:
            body["title"] = title
        if version:
            body["version"] = version
        if overwrite:
            body["overwrite"] = True

        path = "/folders/%s" % uid
        r = await self.client.PUT(path, json=body)
        return r

    async def delete_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        r = await self.client.DELETE(path)
        return r

    async def get_folder_by_id(self, folder_id):
        """

        :param folder_id:
        :return:
        """
        path = "/folders/id/%s" % folder_id
        r = await self.client.GET(path)
        return r

    async def get_folder_permissions(self, uid):
        """

        :return:
        """
        path = "/folders/%s/permissions" % uid
        r = await self.client.GET(path)
        return r

    async def update_folder_permissions(self, uid, items):
        """

        :param uid:
        :param items:
        :return:
        """
        update_folder_permissions_path = "/folders/%s/permissions" % uid
        r = await self.client.POST(update_folder_permissions_path, json=items)
        return r

    async def update_folder_permissions_for_user(self, uid, user_id, items):
        """

        :param uid:
        :param user_id:
        :param items:
            {"permission": "View"} or {"permission": "Edit"} or {"permission": ""}
        :return:
        """

        update_folder_permissions_path_for_user = "/access-control/folders/%s/users/%s" % (uid, user_id)
        r = await self.client.POST(update_folder_permissions_path_for_user, json=items)
        return r
