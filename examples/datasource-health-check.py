"""
Example program for checking whether a data source is healthy.

Documentation: https://github.com/panodata/grafana-client/blob/main/examples/datasource-health-check.rst
"""
import json
import logging
import sys
from distutils.version import LooseVersion
from optparse import OptionParser

import requests

from grafana_client import GrafanaApi
from grafana_client.model import DatasourceHealthResponse
from grafana_client.util import setup_logging

logger = logging.getLogger(__name__)

VERSION_7 = LooseVersion("7")


def run(grafana: GrafanaApi):
    parser = OptionParser()
    parser.add_option("--uid", dest="uid", help="Data source UID")
    (options, args) = parser.parse_args()

    if options.uid:
        datasources = [grafana.datasource.get_datasource_by_uid(options.uid)]
    else:
        datasources = grafana.datasource.list_datasources()

    if not datasources:
        logger.warning(f"No data sources found at {grafana.url}")
        sys.exit(2)

    logger.info(f"Probing {len(datasources)} data sources")

    success = True
    statistics = {"ok": 0, "error": 0, "fatal": 0, "unknown": 0}
    for datasource in datasources:

        logger.info(f"Discovered datasource with uid={datasource['uid']} and type={datasource['type']}")

        # Invoke the health check.
        try:
            health_info = grafana.datasource.health_inquiry(datasource_uid=datasource["uid"])
            if health_info.success:
                statistics["ok"] += 1
            else:
                if health_info.status == "FATAL":
                    statistics["fatal"] += 1
                else:
                    statistics["error"] += 1
        except NotImplementedError as ex:
            message = f"{ex.__class__.__name__}: {ex}"
            health_info = DatasourceHealthResponse(
                uid=datasource["uid"], type=datasource["type"], success=False, status="UNKNOWN", message=message
            )
            statistics["unknown"] += 1
            logger.exception(message)

        # Display the outcome and terminate program based on success state.
        print(json.dumps(health_info.asdict_compact(), indent=2))
        if not health_info.success:
            success = False

    logger.info(f"Statistics: {statistics}")

    if not success:
        sys.exit(1)


if __name__ == "__main__":

    setup_logging(level=logging.DEBUG)

    # Connect to Grafana instance and run health check.
    grafana_client = GrafanaApi.from_env()

    try:
        grafana_client.connect()
    except requests.exceptions.ConnectionError:
        logger.exception("Connecting to Grafana failed")
        raise SystemExit(1)

    grafana_version = LooseVersion(grafana_client.version)
    if grafana_version < VERSION_7:
        raise NotImplementedError(f"Data source health check subsystem not ready for Grafana version {grafana_version}")

    run(grafana_client)
