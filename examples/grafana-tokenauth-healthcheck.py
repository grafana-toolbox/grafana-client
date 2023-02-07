"""
About
=====

Example program for interacting with the Grafana Health API endpoint, in order
to inquire the Grafana version.

Usage
=====

Make sure to adjust the options to `GrafanaApi.from_url(...)` at the bottom of the
file before running the program.

Synopsis
========
::

    source .venv/bin/activate
    python examples/grafana-health.py

"""
from grafana_client import GrafanaApi
from grafana_client.client import TokenAuth


def run_conversation(grafana: GrafanaApi):
    print("Grafana address")
    print(grafana.client.url)

    print("Health check")
    print(grafana.health.check())


if __name__ == "__main__":
    # Connect to custom Grafana instance.
    grafana = GrafanaApi.from_url(
        url="http://localhost:3000/",
        credential=TokenAuth(token="eyJrIjoiMGJIcDBZZVdGV3VNWHYyV1J2dU5lcnVBSW1qYzR2c1MiLCJuIjoiZm9vIiwiaWQiOjF9"),
    )

    # Connect to Grafana instance of Grafana Labs fame.
    # grafana = GrafanaApi(host="play.grafana.org", protocol="https")

    run_conversation(grafana)
