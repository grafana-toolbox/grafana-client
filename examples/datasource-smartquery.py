"""
About
=====

Example program for submitting a query to a data source.

While the ``--query`` option is obligatory, the ``--store`` option is not.
It will be used to designate the ``database`` name, with e.g. InfluxDB,
or the ``metric`` name, with e.g. Prometheus.

Synopsis
========
::

    # Query the InfluxDB 1.x data source on `play.grafana.org`.
    python examples/datasource-smartquery.py --uid=000000002 --query="SHOW RETENTION POLICIES on _internal"
    python examples/datasource-smartquery.py --uid=000000002 --store=site --query="SHOW FIELD KEYS"

    # Query the Prometheus data source on `play.grafana.org`.
    # FIXME: Does not work yet.
    python \
        examples/datasource-smartquery.py --uid=000000008 --store=node_boot_time \
        --query='time() - node_boot_time_seconds{job="node", instance=~"demo.do.prometheus.io:.*"}'

"""
import json
import logging
from optparse import OptionParser

import requests

from grafana_client import GrafanaApi
from grafana_client.model import DatasourceIdentifier
from grafana_client.util import setup_logging

logger = logging.getLogger(__name__)


def run(grafana: GrafanaApi):
    parser = OptionParser()
    parser.add_option("--uid", dest="uid", help="Data source UID")
    parser.add_option("--store", dest="store", help="Database or metric to be addressed")
    parser.add_option("--query", dest="query", help="Query expression")
    (options, args) = parser.parse_args()
    if not options.uid:
        parser.error("Option --uid required")
    if not options.query:
        parser.error("Option --query required")

    # Query the data source by UID.
    response = grafana.datasource.smartquery(
        DatasourceIdentifier(uid=options.uid), expression=options.query, store=options.store
    )

    # Display the outcome in JSON format.
    print(json.dumps(response, indent=2))


if __name__ == "__main__":

    setup_logging(level=logging.DEBUG)

    # Connect to Grafana instance and run health check.
    grafana_client = GrafanaApi.from_url("https://play.grafana.org/")

    try:
        grafana_client.connect()
    except requests.exceptions.ConnectionError:
        logger.exception("Connecting to Grafana failed")
        raise SystemExit(1)

    run(grafana_client)
