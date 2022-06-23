################################
Grafana data source health check
################################


*****
About
*****

``datasource-health-check.py`` is an example program which can be used to
explore the data source health check feature on a remote Grafana instance.

You will have to know the UID of the data source item in order to address
it through the Grafana API.


*****
Usage
*****

Synopsis
========

Inquire the health status of an InfluxDB 1.7 data source on
``play.grafana.org``::

    export GRAFANA_URL=https://play.grafana.org/

    python examples/datasource-health-check.py --uid=000000002

    {
      "uid": "000000002",
      "type": "influxdb",
      "success": true,
      "status": "OK",
      "message": "Success",
      "duration": 0.1559
    }

More examples
=============
Inquire the health status of some other data sources on
``play.grafana.org``::

    export GRAFANA_URL=https://play.grafana.org/

    # Graphite
    # FIXME: Not implemented yet.
    python examples/datasource-health-check.py --uid=000000001

    # InfluxDB 1 / InfluxQL
    python examples/datasource-health-check.py --uid=000000002

    # Not found
    python examples/datasource-health-check.py --uid=000000003

    # Prometheus
    python examples/datasource-health-check.py --uid=000000008
    python examples/datasource-health-check.py --uid=NfggWZLGz

    # Testdata
    python examples/datasource-health-check.py --uid=000000051

On both of those data source items, the new native server-side health check
implementation of Grafana 9+ will be used::

    # Cloudwatch
    python examples/datasource-health-check.py --uid=000000098

    # TwinMaker
    python examples/datasource-health-check.py --uid=qenjJQtnk

