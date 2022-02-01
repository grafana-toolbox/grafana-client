# grafana-client [![Github Actions Test](https://github.com/m0nhawk/grafana_api/workflows/Test/badge.svg)](https://github.com/m0nhawk/grafana_api/actions?query=workflow%3ATest) [![GitHub license](https://img.shields.io/github/license/m0nhawk/grafana_api.svg?style=flat-square)](https://github.com/m0nhawk/grafana_api/blob/master/LICENSE)  [![Codecov](https://img.shields.io/codecov/c/gh/m0nhawk/grafana_api.svg?style=flat-square)](https://codecov.io/gh/m0nhawk/grafana_api/)

[![PyPI](https://img.shields.io/pypi/v/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-api/) [![Conda](https://img.shields.io/conda/v/m0nhawk/grafana_api.svg?style=flat-square)](https://anaconda.org/m0nhawk/grafana_api)

## What is this library for?

Yet another Grafana API library for Python. Support Python 3 only.

## Requirements

You need Python 3 and only the `requests` library installed.

## Quick start

Install the pip package:

```
pip install -U grafana-client
```

And then connect to your Grafana API endpoint:

```python
from grafana_client.grafana_face import GrafanaFace

grafana = GrafanaFace(auth='abcde....', host='api.my-grafana-host.com')

# Create user
user = grafana.admin.create_user({"name": "User", "email": "user@domain.com", "login": "user", "password": "userpassword", "OrgId": 1})

# Change user password
user = grafana.admin.change_user_password(2, "newpassword")

# Search dashboards based on tag
grafana.search.search_dashboards(tag='applications')

# Find a user by email
user = grafana.users.find_user('test@test.com')

# Add user to team 2
grafana.teams.add_team_member(2, user["id"])

# Create or update a dashboard
grafana.dashboard.update_dashboard(dashboard={'dashboard': {...}, 'folderId': 0, 'overwrite': True})

# Delete a dashboard by UID
grafana.dashboard.delete_dashboard(dashboard_uid='abcdefgh')

# Create organization
grafana.organization.create_organization({"name":"new_organization"})
```


## Authentication

There are two ways to autheticate to grafana api. Either use api token or basic auth.

To use admin API you need to use basic auth [as stated here](https://grafana.com/docs/grafana/latest/http_api/admin/)

```python
# Use basic authentication:

grafana = GrafanaFace(
          auth=("username","password"),
          host='api.my-grafana-host.com'
          )

# Use token
grafana = GrafanaFace(
          auth='abcdetoken...',
          host='api.my-grafana-host.com'
          )
```


## Status of REST API realization

Work on API implementation still in progress.

| API | Status |
|---|---|
| Admin | + |
| Alerting | - |
| Alerting Notification Channels | + |
| Annotations | + |
| Authentication | +- |
| Dashboard | + |
| Dashboard Versions | - |
| Dashboard Permissions | + |
| Data Source | + |
| Folder | + |
| Folder Permissions | + |
| Folder/Dashboard Search | +- |
| Organisation | + |
| Other | + |
| Preferences | + |
| Snapshot | + |
| Teams | + |
| User | + |

## Issue tracker

Please report any bugs and enhancement ideas using the `grafana-client` issue tracker:

  https://github.com/m0nhawk/grafana_api/issues

Feel free to also ask questions on the tracker.

## License

`grafana-client` is licensed under the terms of the MIT License (see the file
[LICENSE](LICENSE)).
