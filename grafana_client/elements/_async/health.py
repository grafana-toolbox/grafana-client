from ..base import Base


class Health(Base):
    def __init__(self, client):
        super(Health, self).__init__(client)
        self.client = client

    async def check(self):
        """
        Return Grafana build information, compatible with Grafana, and Amazon Managed Grafana (AMG).

        :return:
        """
        path = "/frontend/settings"
        response = await self.client.GET(path)
        return response.get("buildInfo")
