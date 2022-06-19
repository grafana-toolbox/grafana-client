from .base import Base


class Datasource(Base):
    def __init__(self, client):
        super(Datasource, self).__init__(client)
        self.client = client

    def find_datasource(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/name/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_id(self, datasource_id):
        """
        Warning: This API is deprecated since Grafana v9.0.0 and will be
                 removed in a future release.

        :param datasource_id:
        :return:
        """
        get_datasource_path = "/datasources/%s" % datasource_id
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/name/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_by_uid(self, datasource_uid):
        """

        :param datasource_uid:
        :return:
        """
        get_datasource_path = "/datasources/uid/%s" % datasource_uid
        r = self.client.GET(get_datasource_path)
        return r

    def get_datasource_id_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = "/datasources/id/%s" % datasource_name
        r = self.client.GET(get_datasource_path)
        return r

    def get(self, datasource_id: str = None, datasource_uid: str = None, datasource_name: str = None):
        """
        Get dashboard by either datasource_id, datasource_uid, or datasource_name.
        """
        if datasource_id:
            datasource = self.get_datasource_by_id(datasource_id)
        elif datasource_uid:
            datasource = self.get_datasource_by_uid(datasource_uid)
        elif datasource_name:
            datasource = self.get_datasource_by_name(datasource_name)
        else:
            raise KeyError("Either datasource_id or datasource_name must be given")
        return datasource

    def create_datasource(self, datasource):
        """

        :param datasource:
        :return:
        """
        create_datasources_path = "/datasources"
        r = self.client.POST(create_datasources_path, json=datasource)
        return r

    def update_datasource(self, datasource_id, datasource):
        """

        :param datasource_id:
        :param datasource:
        :return:
        """
        update_datasource = "/datasources/%s" % datasource_id
        r = self.client.PUT(update_datasource, json=datasource)
        return r

    def list_datasources(self):
        """

        :return:
        """
        list_datasources_path = "/datasources"
        r = self.client.GET(list_datasources_path)
        return r

    def delete_datasource_by_id(self, datasource_id):
        """
        Warning: This API is deprecated since Grafana v9.0.0 and will be
                 removed in a future release.

        :param datasource_id:
        :return:
        """
        delete_datasource = "/datasources/%s" % datasource_id
        r = self.client.DELETE(delete_datasource)
        return r

    def delete_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        delete_datasource = "/datasources/name/%s" % datasource_name
        r = self.client.DELETE(delete_datasource)
        return r

    def delete_datasource_by_uid(self, datasource_uid):
        """

        :param datasource_uid:
        :return:
        """
        delete_datasource = "/datasources/uid/%s" % datasource_uid
        r = self.client.DELETE(delete_datasource)
        return r

    def get_datasource_proxy_data(
        self, datasource_id, query_type="query", version="v1", expr=None, time=None, start=None, end=None, step=None
    ):
        """

        :param datasource_id:
        :param version: api_version currently v1
        :param query_type: query_range |query
        :param expr: expr to query

        :return: r (dict)
        """
        get_datasource_path = "/datasources/proxy/{0}" "/api/{1}/{2}?query={3}".format(
            datasource_id, version, query_type, expr
        )
        if query_type == "query_range":
            get_datasource_path = get_datasource_path + "&start={0}&end={1}&step={2}".format(start, end, step)
        else:
            get_datasource_path = get_datasource_path + "&time={}".format(time)
        r = self.client.GET(get_datasource_path)
        return r
