"""
Demo program for checking whether a data source is healthy.

Documentation: See `datasource-health.rst`.
"""
import json
import logging
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=Warning, message="distutils Version classes are deprecated")
from distutils.version import LooseVersion
from optparse import OptionParser

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError
from grafana_client.knowledge import datasource_factory
from grafana_client.model import DatasourceModel
from grafana_client.util import grafana_client_factory, setup_logging

logger = logging.getLogger(__name__)


VERSION_7 = LooseVersion("7")
VERSION_8 = LooseVersion("8")
VERSION_9 = LooseVersion("9")


def ensure_datasource(grafana: GrafanaApi, datasource: DatasourceModel):
    """
    Ensure data source exists and is configured like desired.

    Either create the data source, or update it. The data source name will be
    used as data source identified.
    """

    datasource_name = datasource.name

    # Create data source.
    datasource = datasource.asdict()
    try:
        logger.info(f"Creating data source '{datasource_name}'")
        datasource = grafana.datasource.create_datasource(datasource)["datasource"]
    except GrafanaClientError as ex:

        # When data source already exists, update data source.
        if ex.status_code == 409:
            logger.info(f"Data source already exists: {ex.response}. Updating.")
            datasource_existing = grafana.datasource.get_datasource_by_name(datasource_name=datasource_name)
            datasource = grafana.datasource.update_datasource(datasource_existing["id"], datasource)["datasource"]
        else:
            logger.error(
                f"Failed to create or update data source '{datasource}'. "
                f"Reason: {ex.message}. Response: {ex.response}"
            )
            raise
    return datasource


def health_inquiry(grafana: GrafanaApi, datasource: DatasourceModel, grafana_version: LooseVersion = None):
    """
    Add a data source dynamically and run a data source health check on it.
    Be graceful if it exists already.
    """

    # Create data source.
    datasource = ensure_datasource(grafana, datasource)
    datasource_id = datasource["id"]
    datasource_uid = datasource["uid"]

    # Resolve data source by UID.
    datasource = grafana.datasource.get(datasource_id=datasource_id)

    # Check data source health.
    health = None
    if True or grafana_version and grafana_version >= VERSION_9:
        try:
            health = grafana.datasource.health(datasource_uid=datasource_uid)
        except GrafanaClientError as ex:
            logger.warning(f"Native data source health check for uid={datasource_uid} failed: {ex}. Response: {ex.response}")
            if ex.status_code != 404:
                raise

    if health is None:
        health = grafana.datasource.health_check(datasource=datasource)

    # Delete data source again.
    grafana.datasource.delete_datasource_by_id(datasource_id)

    return health.for_response()


def prometheus_demo(grafana: GrafanaApi):
    datasource = DatasourceModel(
        name="probe-prometheus", type="prometheus", url="http://host.docker.internal:9090", access="server"
    )
    health_info = health_inquiry(grafana, datasource)
    return health_info


def run_healthcheck(grafana: GrafanaApi, grafana_version: LooseVersion = None):

    # When called without options, invoke the Prometheus demo.
    if len(sys.argv) == 1:
        if grafana_version < VERSION_8:
            raise NotImplementedError(
                f"Data source health check subsystem on Grafana version {grafana_version} not supported for Prometheus"
            )
        health_info = prometheus_demo(grafana)

    # When called with options,
    else:
        # parse them, and
        parser = OptionParser()
        parser.add_option("--type", dest="type", help="Data source type")
        parser.add_option("--url", dest="url", help="Data source URL")
        (options, args) = parser.parse_args()
        if (not options.type or not options.url) and not options.type == "testdata":
            parser.error("Options --type and --url required")

        # Sanity checks
        if options.type == "prometheus" and grafana_version < VERSION_8:
            raise NotImplementedError(
                f"Data source health check subsystem on Grafana version {grafana_version} not supported for Prometheus"
            )

        # ... create a dynamic data source with the corresponding values.
        name = f"probe-{options.type}"
        datasource = DatasourceModel(name=name, type=options.type, url=options.url, access="server")
        datasource = datasource_factory(datasource)

        # Invoke the health check.
        health_info = health_inquiry(grafana, datasource, grafana_version=grafana_version)

    # Display the outcome and terminate program based on success state.
    print(json.dumps(health_info, indent=2))
    if not health_info["success"]:
        sys.exit(1)


if __name__ == "__main__":

    setup_logging(level=logging.DEBUG)

    grafana_url = os.environ.get("GRAFANA_URL", "http://localhost:3000")

    # Connect to Grafana instance and run health check.
    grafana_client = grafana_client_factory(grafana_url=grafana_url, grafana_token=os.environ.get("GRAFANA_TOKEN"))

    grafana_info = grafana_client.health.check()
    grafana_version = LooseVersion(grafana_info["version"])
    logger.info(f"Connected to Grafana version {grafana_version} at {grafana_url}")

    if grafana_version < VERSION_7:
        raise NotImplementedError(f"Data source health check subsystem not ready for Grafana version {grafana_version}")

    run_healthcheck(grafana_client, grafana_version=grafana_version)
