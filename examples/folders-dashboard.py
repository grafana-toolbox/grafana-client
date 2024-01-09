"""
About
=====

Example program for listing folders and getting a dashboard of a remote Grafana
instance. By default, it uses `play.grafana.org`. Please adjust to your needs.


Synopsis
========
::

    source .venv/bin/activate
    python examples/folders-dashboard.py | jq
"""

import json
import sys
from time import perf_counter

from grafana_client import GrafanaApi


def main():
    before = perf_counter()
    # Connect to public Grafana instance of Grafana Labs fame.
    grafana = GrafanaApi(host="play.grafana.org")

    print("## All folders on play.grafana.org", file=sys.stderr)
    folders = grafana.folder.get_all_folders()
    print(json.dumps(folders, indent=2))

    for folder in folders[:4]:
        print(f"## Dashboard with UID {folder['uid']} at play.grafana.org", file=sys.stderr)
        dashboard = grafana.dashboard.get_dashboard(folder["uid"])
        print(json.dumps(dashboard, indent=2))

    print(f"## Completed in {perf_counter() - before}s", file=sys.stderr)


if __name__ == "__main__":
    main()
