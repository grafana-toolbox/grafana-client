"""
Example program for probing whether a data source is healthy.

Documentation: https://github.com/panodata/grafana-client/blob/main/examples/datasource-health-probe.rst
"""
import json
import logging
import sys
from distutils.version import LooseVersion
from optparse import OptionParser

import requests

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError
from grafana_client.knowledge import datasource_factory
from grafana_client.model import DatasourceModel
from grafana_client.util import setup_logging

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


def health_probe(grafana: GrafanaApi, datasource: DatasourceModel):
    """
    Add a data source dynamically, run a data source health check on it,
    and delete it again. Be graceful if the data source exists already.
    """
    # Create data source.
    datasource = ensure_datasource(grafana, datasource)
    datasource_uid = datasource["uid"]

    # Invoke the health check.
    health_info = grafana.datasource.health_inquiry(datasource_uid=datasource_uid)

    # Delete data source again.
    grafana.datasource.delete_datasource_by_uid(datasource_uid)

    return health_info.asdict_compact()


def prometheus_demo(grafana: GrafanaApi):
    datasource = DatasourceModel(
        name="probe-prometheus", type="prometheus", url="http://host.docker.internal:9090", access="server"
    )
    health_info = health_probe(grafana, datasource)
    return health_info


def run(grafana: GrafanaApi, grafana_version: LooseVersion = None):

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

        # Invoke the health probe.
        health_info = health_probe(grafana, datasource)

    # Display the outcome and terminate program based on success state.
    print(json.dumps(health_info, indent=2))
    if not health_info["success"]:
        sys.exit(1)


if __name__ == "__main__":

    setup_logging(level=logging.DEBUG)

    # Connect to Grafana instance and run health probe.
    grafana_client = GrafanaApi.from_env()

    try:
        grafana_client.connect()
    except requests.exceptions.ConnectionError:
        logger.exception("Connecting to Grafana failed")
        raise SystemExit(1)

    grafana_version = LooseVersion(grafana_client.version)
    if grafana_version < VERSION_7:
        raise NotImplementedError(f"Data source health check subsystem not ready for Grafana version {grafana_version}")

    run(grafana_client, grafana_version=grafana_version)
