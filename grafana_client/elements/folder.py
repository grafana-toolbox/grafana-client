from .base import Base


class Folder(Base):
    def __init__(self, client):
        super(Folder, self).__init__(client)
        self.client = client

    def get_all_folders(self):
        """

        :return:
        """
        path = "/folders"
        r = self.client.GET(path)
        return r

    def get_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        r = self.client.GET(path)
        return r

    def create_folder(self, title, uid=None):
        """

        :param title:
        :param uid:
        :return:
        """
        json_data = dict(title=title)
        if uid is not None:
            json_data["uid"] = uid
        return self.client.POST("/folders", json=json_data)

    def update_folder(self, uid, title=None, version=None, overwrite=False, new_uid=None):
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
        r = self.client.PUT(path, json=body)
        return r

    def delete_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        r = self.client.DELETE(path)
        return r

    def get_folder_by_id(self, folder_id):
        """

        :param folder_id:
        :return:
        """
        path = "/folders/id/%s" % folder_id
        r = self.client.GET(path)
        return r

    def get_folder_permissions(self, uid):
        """

        :return:
        """
        path = "/folders/%s/permissions" % uid
        r = self.client.GET(path)
        return r

    def update_folder_permissions(self, uid, items):
        """

        :param uid:
        :param items:
        :return:
        """
        update_folder_permissions_path = "/folders/%s/permissions" % uid
        r = self.client.POST(update_folder_permissions_path, json=items)
        return r
