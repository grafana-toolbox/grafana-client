from .base import Base


class Search(Base):
    def __init__(self, client):
        super(Search, self).__init__(client)
        self.client = client

    def search_dashboards(
        self,
        query=None,
        tag=None,
        type_=None,
        dashboard_ids=None,
        folder_ids=None,
        starred=None,
        limit=None,
    ):
        """

        :param query:
        :param tag:
        :param type_:
        :param dashboard_ids:
        :param folder_ids:
        :param starred:
        :param limit:
        :return:
        """
        list_dashboard_path = "/search"
        params = []

        if query:
            params.append("query=%s" % query)

        if tag:
            params.append("tag=%s" % tag)

        if type_:
            params.append("type=%s" % type_)

        if dashboard_ids:
            params.append("dashboardIds=%s" % dashboard_ids)

        if folder_ids:
            params.append("folderIds=%s" % folder_ids)

        if starred:
            params.append("starred=%s" % starred)

        if limit:
            params.append("limit=%s" % limit)

        list_dashboard_path += "?"
        list_dashboard_path += "&".join(params)

        r = self.client.GET(list_dashboard_path)
        return r
