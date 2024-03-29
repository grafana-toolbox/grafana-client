from .base import Base


class Snapshots(Base):
    def __init__(self, client):
        super(Snapshots, self).__init__(client)
        self.client = client

    def create_new_snapshot(
        self,
        dashboard=None,
        name=None,
        expires=None,
        external=None,
        key=None,
        delete_key=None,
    ):
        """

        :param dashboard:  Required. The complete dashboard model.
        :param name: Optional. snapshot name
        :param expires: Optional. When the snapshot should expire in seconds. 3600 is 1 hour, 86400 is 1 day.
                        Default is to never expire.
        :param external: Optional. Save the snapshot on an external server rather than locally. Default is false.
        :param key: Optional. Define the unique key. Required if external is true.
        :param deleteKey: Optional. Unique key used to delete the snapshot. It is different from the key so that only
                          the creator can delete the snapshot. Required if external is true.
        :return:
        """

        path = "/snapshots"
        post_json = {"dashboard": dashboard}
        if name:
            post_json["name"] = name
        if expires:
            post_json["expires"] = expires
        if external:
            post_json["external"] = external
        if key:
            post_json["key"] = key
        if delete_key:
            post_json["deleteKey"] = delete_key

        return self.client.POST(path, json=post_json)

    def get_dashboard_snapshots(self):
        """

        :return:
        """
        path = "/dashboard/snapshots"
        return self.client.GET(path)

    def get_snapshot_by_key(self, key):
        """

        :param key:
        :return:
        """
        path = "/snapshots/%s" % key
        return self.client.GET(path)

    def delete_snapshot_by_key(self, snapshot_id=None):
        """

        :param snapshot_id:
        :return:
        """
        path = f"/snapshots/{snapshot_id}"
        return self.client.DELETE(path)

    def delete_snapshot_by_delete_key(self, snapshot_delete_key=None):
        """

        :param snapshot_delete_key:
        :return:
        """
        path = f"/snapshots-delete/{snapshot_delete_key}"
        return self.client.GET(path)
