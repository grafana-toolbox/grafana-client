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
from grafana_client.util import setup_logging

logger = logging.getLogger(__name__)

VERSION_7 = LooseVersion("7")


def run(grafana: GrafanaApi):
    parser = OptionParser()
    parser.add_option("--uid", dest="uid", help="Data source UID")
    (options, args) = parser.parse_args()
    if not options.uid:
        parser.error("Option --uid required")

    # Invoke the health check.
    health_info = grafana.datasource.health_inquiry(datasource_uid=options.uid)

    # Display the outcome and terminate program based on success state.
    print(json.dumps(health_info.asdict_compact(), indent=2))
    if not health_info.success:
        sys.exit(1)


if __name__ == "__main__":

    setup_logging(level=logging.DEBUG)

    # Connect to Grafana instance and run health check.
    grafana_client = GrafanaApi.from_env()

    try:
        grafana_client.connect()
    except requests.exceptions.ConnectionError as ex:
        raise SystemExit(1)

    grafana_version = LooseVersion(grafana_client.version)
    if grafana_version < VERSION_7:
        raise NotImplementedError(f"Data source health check subsystem not ready for Grafana version {grafana_version}")

    run(grafana_client)
