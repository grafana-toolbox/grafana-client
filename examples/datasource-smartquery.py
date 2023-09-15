"""
About
=====

Example program for submitting a query to a data source.

While the ``--query`` option is obligatory, the ``--attr`` option is not.
It will be used to designate the ``database`` name, with e.g. InfluxDB,
or the ``queryType`` name, with e.g. Loki.

Synopsis
========
::
    # Query the InfluxDB 1.x data source on `play.grafana.org`.
    python examples/datasource-smartquery.py --uid=000000002 --query="SHOW RETENTION POLICIES on _internal"
    python examples/datasource-smartquery.py --uid=000000002 --attr "database:site" --query="SHOW FIELD KEYS"
    python examples/datasource-smartquery.py --uid 000000002 --query "SELECT sum(\"value\") FROM \"logins.count\" WHERE time >= now() - 5m and time <= now() GROUP BY time(10s) fill(null)"

    # Query the InfluxDB+flux on https://play.grafana.org
    # fix me : query invalid !
    python examples/datasource-smartquery.py \
        --uid M3k6ZPrnz \
        --query "from(bucket: \"HyperEncabulator\")\\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\\n    |> filter(fn: (r) => r[\"_measurement\"] == \"TemperatureData\")\\n    |> filter(fn: (r) => r[\"MeasType\"] == \"setpoint\" or r[\"MeasType\"] == \"actual\")\\n    |> filter(fn: (r) => r[\"Tank\"] == \"A5\")\\n    |> filter(fn: (r) => r[\"_field\"] == \"Temperature\")\\n    |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\\n    |> yield(name: \"mean\")"
    # fix-me
        --query "from(bucket: \"example-bucket\")\\n  |> range(start: -1h)\\n  |> filter(fn: (r) => r._measurement == \"example-measurement\" and r._field == \"example-field\")"

    # Query the Graphite datasource on https://play.grafana.org
    python examples/datasource-smartquery.py --uid 000000001 --query "aliasByNode(apps.fakesite.web_server_02.counters.requests.count,2)"

    # Query the Prometheus data source on `play.grafana.org`.
    python examples/datasource-smartquery.py \
        --uid=000000008 \
        --query='time() - node_boot_time_seconds{job="node", instance=~"demo.do.prometheus.io:.*"}'

    # Query the Loki data source on `play.grafana.org`.
    python examples/datasource-smartquery.py \
        --uid=NX9d1VH7k \
        --query "bytes_over_time({filename=~\".+/json_access.+\", job=~\".*\", instance=~\".*\"}[5m])" \
        --attr "queryType:instant"
    python examples/datasource-smartquery.py \
        --uid=NX9d1VH7k \
        --query "sum by (status) (count_over_time({filename=~\".+/json_access.+\", job=~\".*\", instance=~\".*\"} | json |  __error__=\"\" [5m]))" \
        --attr "legendFormat:HTTP Status {{status}}"

"""  # noqa: E501
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
    # replace by --attr "database:<store>" or --attr "metric:<metric>"
    # parser.add_option("--store", dest="store", help="Database or metric to be addressed")
    parser.add_option("--query", dest="query", help="Query expression")
    parser.add_option("--attr", dest="attrs", action="append", help="key:value pair attribute to send into query")
    (options, args) = parser.parse_args()
    if not options.uid:
        parser.error("Option --uid required")
    if not options.query:
        parser.error("Option --query required")

    attributes = {}
    if options.attrs is not None and len(options.attrs) > 0:
        for attr in options.attrs:
            (key, val) = attr.split(":")
            attributes[key] = val

    # replace double backslash chars by their values \\n => \n
    query = bytes(options.query, "utf-8").decode("unicode_escape")
    # Query the data source by UID.
    response = grafana.datasource.smartquery(
        DatasourceIdentifier(uid=options.uid),
        query,
        attrs=attributes,
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
