"""
About
=====

Example program for interacting with the Grafana Service Account.

Usage
=====

Make sure to adjust `GrafanaApi` options at the bottom of the
file.
And replace aaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa with the uid of the folder where you want to add the service account.

Synopsis
========
::

    source .venv/bin/activate
    python examples/service-account.py

"""

import uuid

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError


def run_conversation(grafana: GrafanaApi):
    # print("Grafana address")
    # print(grafana.client.url)

    # print("Health check")
    # print(grafana.health.check())

    print("Create Service Account")
    sa = {"name": "Sytem Account DEMO", "role": "Viewer"}

    # Add a new service account
    try:
        response = grafana.serviceaccount.create(sa)
        print(response)
    except GrafanaClientError as ex:
        print(f"ERROR: {ex}")

    # Add a new token to service account, you need to writedown the token['key'] to use it later
    # Genera an UUID
    uuid_to_token = uuid.uuid4()
    token_name = "%s" % (uuid_to_token)

    try:
        token = grafana.serviceaccount.create_token(response["id"], {"name": token_name})
        print(token)
    except GrafanaClientError as ex:
        print(f"ERROR: {ex}")

    # Add Viewer permissions to service account created to folder with uid aaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
    uid_folder = "aaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    permissions = {"permission": "View"}
    sa_id = response["id"]
    grafana.folder.update_folder_permissions_for_user(uid_folder, sa_id, permissions)

    # Search service account by name
    search_sa = grafana.serviceaccount.search_one(service_account_name="Sytem Account DEMO")
    print(search_sa)


if __name__ == "__main__":
    # Connect to custom Grafana instance.
    grafana = GrafanaApi.from_url(url="localhost:3000", credential=("admin", "admin"))

    run_conversation(grafana)
