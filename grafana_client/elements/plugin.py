import logging

from .base import Base


class Plugin(Base):
    def __init__(self, client):
        super(Plugin, self).__init__(client)
        self.client = client
        self.logger = logging.getLogger(__name__)

    def get_installed_plugins(self):
        """
        :return:
        """
        path = "/plugins?embedded=0"
        r = self.client.GET(path)
        return r

    def install_plugin(self, pluginId, version, errors="raise"):
        """
        : return:
        """
        try:
            path = "/plugins/%s/install" % pluginId
            r = self.client.POST(path, json={"version": version})
            return r
        except Exception as ex:
            if errors == "raise":
                raise
            elif errors == "ignore":
                self.logger.info(f"Skipped installing plugin {pluginId}: {ex}")
            else:
                raise ValueError(f"error={errors} is invalid")
        return None

    def uninstall_plugin(self, pluginId, errors="raise"):
        """
        : return:
        """
        try:
            path = "/plugins/%s/uninstall" % pluginId
            r = self.client.POST(path)
            return r
        except Exception as ex:
            if errors == "raise":
                raise
            elif errors == "ignore":
                self.logger.info(f"Skipped uninstalling plugin {pluginId}: {ex}")
            else:
                raise ValueError(f"error={errors} is invalid")
        return None

    def health_check_plugin(self, pluginId):
        """
        :return:
        """
        path = "/plugins/%s/health" % pluginId
        r = self.client.GET(path)
        return r

    def get_plugin_metrics(self, pluginId):
        """
        : return:
        """
        path = "/plugins/%s/metrics" % pluginId
        r = self.client.GET(path)
        return r
