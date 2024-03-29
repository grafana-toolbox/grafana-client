import logging

from grafana_client.client import GrafanaClientError

from .base import Base


class Plugin(Base):
    def __init__(self, client):
        super(Plugin, self).__init__(client)
        self.client = client
        self.logger = logging.getLogger(__name__)

    def list(self):
        """
        Return list of all installed plugins.
        """
        path = "/plugins?embedded=0"
        return self.client.GET(path)

    def by_id(self, plugin_id):
        """
        Return single plugin item selected by plugin identifier.
        """
        plugins = self.list()
        return get_plugin_by_id(plugin_list=plugins, plugin_id=plugin_id)

    def install(self, plugin_id, version=None, errors="raise"):
        """
        Install a 3rd-party plugin from the plugin store.
        """
        try:
            path = "/plugins/%s/install" % plugin_id
            # Unfortunately, this endpoint may respond with an empty JSON,
            # which needs compensation, because it does not decode well.
            return self.client.POST(path, json={"version": version}, accept_empty_json=True)
        except GrafanaClientError as ex:
            # Ignore `Client Error 409: Plugin already installed`.
            if "409" not in str(ex):
                raise
        except Exception as ex:
            if errors == "raise":
                raise
            elif errors == "ignore":
                self.logger.warning(f"Problem installing plugin {plugin_id}: {ex}")
            else:
                raise ValueError(f"error={errors} is invalid")
        return None

    def uninstall(self, plugin_id, errors="raise"):
        """
        Uninstall a 3rd-party plugin from the Grafana instance.
        """
        try:
            path = "/plugins/%s/uninstall" % plugin_id
            # Unfortunately, this endpoint may respond with an empty JSON,
            # which needs compensation, because it does not decode well.
            return self.client.POST(path, accept_empty_json=True)
        except Exception as ex:
            if errors == "raise":
                raise
            elif errors == "ignore":
                self.logger.warning(f"Problem uninstalling plugin {plugin_id}: {ex}")
            else:
                raise ValueError(f"error={errors} is invalid")
        return None

    def health(self, plugin_id):
        """
        Run a health check probe on the designated plugin.
        """
        path = "/plugins/%s/health" % plugin_id
        return self.client.GET(path)

    def metrics(self, plugin_id):
        """
        Inquire metrics of the designated plugin.
        """
        path = "/plugins/%s/metrics" % plugin_id
        return self.client.GET(path)


def get_plugin_by_id(plugin_list, plugin_id):
    """
    Helper function to filter plugin list by identifier.
    """
    try:
        return next(item for item in plugin_list if item["id"] == plugin_id)
    except StopIteration:
        raise KeyError(f"Plugin not found: {plugin_id}")
