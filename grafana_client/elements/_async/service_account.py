"""
https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/
https://grafana.com/docs/grafana/latest/administration/service-accounts/
https://grafana.com/docs/grafana/latest/developers/http_api/create-api-tokens-for-org/
"""

from ..base import Base


class ServiceAccount(Base):
    def __init__(self, client):
        super(ServiceAccount, self).__init__(client)
        self.client = client
        self.path = "/serviceaccounts"

    async def get(self, service_account_id):
        """
        Get service account by id.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#get-a-service-account-by-id

        :param service_account_id:
        :return:
        """
        get_actual_user_path = "/serviceaccounts/%s?accesscontrol=true" % (service_account_id)
        return await self.client.GET(get_actual_user_path)

    async def create(self, service_account):
        """
        Create service account.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#create-service-account

        :param service_account: {"name": "string", "role": "string"}
        :return:
        """
        create_service_account_path = "/serviceaccounts/"
        return await self.client.POST(create_service_account_path, json=service_account)

    async def update(self, service_account_id, service_account):
        """
        Update service account by id.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#update-service-account

        :param service_account_id:
        :param service_account: {"name": "string", "role": "string"}
        :return:
        """
        path = "/serviceaccounts/%s" % service_account_id
        return await self.client.PATCH(path, json=service_account)

    async def delete(self, service_account_id):
        """
        Delete service account.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#delete-service-account

        :param service_account_id:
        :return:
        """

        delete_service_account_path = "/serviceaccounts/%s" % (service_account_id)
        return await self.client.DELETE(delete_service_account_path)

    async def get_tokens(self, service_account_id):
        """
        Get service account tokens.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#get-service-account-tokens

        :param service_account_id:
        :return:
        """
        service_account_tokens_path = "/serviceaccounts/%s/tokens" % (service_account_id)
        return await self.client.GET(service_account_tokens_path)

    async def create_token(self, service_account_id, content):
        """
        Create service account tokens
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#create-service-account-tokens

        :param service_account_id:
        :param service_account_name:
        :return:
        """
        create_service_account_token_path = "/serviceaccounts/%s/tokens" % (service_account_id)
        return await self.client.POST(create_service_account_token_path, json=content)

    async def delete_token(self, service_account_id, service_account_token_id):
        """
        Delete service account tokens.
        https://grafana.com/docs/grafana/latest/developers/http_api/serviceaccount/#delete-service-account-tokens

        :param service_account_id:
        :param service_account_token_id:
        :return:
        """
        delete_service_account_token_path = "/serviceaccounts/%s/tokens/%s" % (
            service_account_id,
            service_account_token_id,
        )
        return await self.client.DELETE(delete_service_account_token_path)

    async def search(self, query=None, page=None, perpage=None):
        """

        :return:
        """
        list_of_sa = []
        sa_on_page = None
        show_sa_path = "/serviceaccounts/search"
        params = []
        if query:
            params.append("query=%s" % query)

        if page:
            iterate = False
            params.append("page=%s" % page)
        else:
            iterate = True
            params.append("page=%s")
            page = 1

        if perpage:
            params.append("perpage=%s" % perpage)

        show_sa_path += "?"
        show_sa_path += "&".join(params)
        if iterate:
            while True:
                url = show_sa_path % page
                sa_on_page = await self.client.GET(url)
                list_of_sa.append(sa_on_page)
                if not sa_on_page["serviceAccounts"]:
                    break
                page += 1
        else:
            sa_on_page = await self.client.GET(show_sa_path)
            list_of_sa.append(sa_on_page)

        return list_of_sa

    async def search_one(self, service_account_name=""):
        """
        Find a single service account by name. Raises errors on multiple or no matches.

        :param service_account_name:
        :return:
        """
        s = await self.search(query=service_account_name)[0]
        if s["totalCount"] == 1:
            return s["serviceAccounts"][0]
        elif s["totalCount"] > 1:
            raise ValueError("More than one service account matched")
        else:
            raise ValueError("No service account matched")
