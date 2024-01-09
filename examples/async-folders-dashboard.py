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

import asyncio
import json
import sys
from time import perf_counter

from grafana_client import AsyncGrafanaApi


async def fetch_dashboard(grafana, uid):
    print(f"## Dashboard with UID {uid} at play.grafana.org", file=sys.stderr)
    dashboard = await grafana.dashboard.get_dashboard(uid)
    print(json.dumps(dashboard, indent=2))


async def main():
    before = perf_counter()
    # Connect to public Grafana instance of Grafana Labs fame.
    grafana = AsyncGrafanaApi(host="play.grafana.org")

    print("## All folders on play.grafana.org", file=sys.stderr)
    folders = await grafana.folder.get_all_folders()
    print(json.dumps(folders, indent=2))

    tasks = []

    for folder in folders:
        if folder["id"] > 0:
            tasks.append(fetch_dashboard(grafana, folder["uid"]))
            if len(tasks) == 4:
                break

    await asyncio.gather(*tasks)
    print(f"## Completed in {perf_counter() - before}s", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
