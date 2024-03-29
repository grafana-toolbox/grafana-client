from .base import Base


class Alerting(Base):
    def __init__(self, client):
        super(Alerting, self).__init__(client)
        self.client = client

    def get_alertrule(self, folder_name, alertrule_name):
        """
        :param folder_name:
        :param alertrule_name:
        :return:
        """
        get_alertrule_path = "/ruler/grafana/api/v1/rules/%s/%s" % (folder_name, alertrule_name)
        return self.client.GET(get_alertrule_path)

    def create_alertrule(self, folder_name, alertrule):
        """
        :param folder_name:
        :param alertrule:
        :return:
        """
        create_alertrule_path = "/ruler/grafana/api/v1/rules/%s" % folder_name
        return self.client.POST(create_alertrule_path, json=alertrule)

    def update_alertrule(self, folder_name, alertrule):
        """
        @param folder_name:
        @param alertrule:
        @return:
        """

        update_alertrule_path = "/ruler/grafana/api/v1/rules/%s" % folder_name
        return self.client.POST(update_alertrule_path, json=alertrule)

    def delete_alertrule(self, folder_name, alertrule_name):
        """
        :param folder_name:
        :param alertrule_name:
        @return:
        """

        delete_alertrule_path = "/ruler/grafana/api/v1/rules/%s/%s" % (folder_name, alertrule_name)
        return self.client.DELETE(delete_alertrule_path)
