"""
About
=====

Example program for interacting with the Grafana Teams API.
It will need `teams:{create,read}` permissions to create a team and inquire the
list of existing teams afterwards.

Usage
=====

Make sure to adjust `GrafanaApi(auth=, host=)` options at the bottom of the
file.

Synopsis
========
::

    source .venv/bin/activate
    python examples/team.py

"""
import json

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError


def run_conversation(grafana: GrafanaApi):

    print("Grafana address")
    print(grafana.client.url)

    print("Health check")
    print(grafana.health.check())

    print("Create team")
    team = {"name": "Testdrive Team", "email": "email@example.org"}
    try:
        response = grafana.teams.add_team(team)
        print(response)
    except GrafanaClientError as ex:
        if ex.status_code == 409:
            print(f"Team already exists: {ex.response}")
        else:
            print(f"ERROR: {ex}")

    print("Search teams")
    try:
        response = grafana.teams.search_teams()
        print(jd(response))
    except GrafanaClientError as ex:
        print(f"ERROR: {ex}")


def jd(data):
    return json.dumps(data, indent=2)


if __name__ == "__main__":

    # Connect to custom Grafana instance.
    grafana = GrafanaApi(
        auth=("admin", "admin"),
        host="localhost:3000",
    )

    # Connect to Grafana instance of Grafana Labs fame.
    # You will see permission errors on this, as you will probably have none of
    # `teams:{create,read}` on Grafana's server, let alone without authentication.
    # grafana = GrafanaApi(host="play.grafana.org", protocol="https")

    run_conversation(grafana)
