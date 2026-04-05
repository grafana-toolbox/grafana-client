from grafana_client.util import as_bool, format_param_value

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
        dashboard_uids=None,
        folder_ids=None,
        folder_uids=None,
        starred=None,
        limit=None,
        page=None,
    ):
        """

        :param query:
        :param tag:
        :param type_:
        :param dashboard_ids:
        :param dashboard_uids:
        :param folder_ids:
        :param folder_uids:
        :param starred:
        :param limit:
        :param page:
        :return:
        """
        list_dashboard_path = "/search"
        params = {}

        if query is not None:
            params["query"] = query

        if tag is not None:
            params["tag"] = format_param_value(tag)

        if type_ is not None:
            params["type"] = type_

        if dashboard_ids is not None:
            params["dashboardIds"] = format_param_value(dashboard_ids)

        if dashboard_uids is not None:
            params["dashboardUIDs"] = format_param_value(dashboard_uids)

        if folder_ids is not None:
            params["folderIds"] = format_param_value(folder_ids)

        if folder_uids is not None:
            params["folderUIDs"] = format_param_value(folder_uids)

        if as_bool(starred):
            params["starred"] = "true"

        if limit is not None:
            params["limit"] = limit

        if page is not None:
            params["page"] = page

        return self.client.GET(list_dashboard_path, params=params)
