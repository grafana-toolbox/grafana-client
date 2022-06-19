import json
import sys

from grafana_client import GrafanaApi


def main():

    # Connect to Grafana instance of Grafana Labs fame.
    grafana = GrafanaApi(host="play.grafana.org")

    print("## All folders on play.grafana.org", file=sys.stderr)
    folders = grafana.folder.get_all_folders()
    print(json.dumps(folders, indent=2))

    # print("## Dashboard with UID 000000012 at play.grafana.org", file=sys.stderr)
    # dashboard_000000012 = grafana.dashboard.get_dashboard("000000012")
    # print(dashboard_000000012)


if __name__ == "__main__":
    main()
