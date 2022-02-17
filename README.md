# grafana-client

[![Tests](https://github.com/panodata/grafana-client/workflows/Test/badge.svg)](https://github.com/panodata/grafana-client/actions?query=workflow%3ATest)
[![Test coverage](https://img.shields.io/codecov/c/gh/panodata/grafana-client.svg?style=flat-square)](https://codecov.io/gh/panodata/grafana-client/)
[![License](https://img.shields.io/github/license/panodata/grafana-client.svg?style=flat-square)](https://github.com/panodata/grafana-client/blob/main/LICENSE) 

[![PyPI](https://img.shields.io/pypi/v/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![Status](https://img.shields.io/pypi/status/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![Downloads](https://img.shields.io/pypi/dm/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
<!-- [![Conda](https://img.shields.io/conda/v/panodata/grafana-client.svg?style=flat-square)](https://anaconda.org/panodata/grafana-client) -->


## About

A client library for the Grafana HTTP API, written in Python.

## History

The library was originally conceived by [Andrew Prokhorenkov] and contributors
as [grafana_api]. Thank you very much for your efforts!

At [future maintenance of `grafana_api`], we discussed the need for a fork
because the repository stopped receiving updates since more than a year.

While forking it, we renamed the package to `grafana-client` and slightly
trimmed the module namespace.



## Getting started

Install the package from PyPI.

```
pip install grafana-client --upgrade
```

Connect to your Grafana API endpoint using the `GrafanaApi` class.

```python
from grafana_client import GrafanaApi

grafana = GrafanaApi(auth='eyJrIjoiWHg...dGJpZCI6MX0=', host='grafana.example.org')

# Create user
user = grafana.admin.create_user(
    {"name": "User", "email": "user@example.org", "login": "user", "password": "userpassword", "OrgId": 1})

# Change user password
user = grafana.admin.change_user_password(2, "newpassword")

# Search dashboards based on tag
grafana.search.search_dashboards(tag='applications')

# Find a user by email
user = grafana.users.find_user('test@example.org')

# Add user to team 2
grafana.teams.add_team_member(2, user["id"])

# Create or update a dashboard
grafana.dashboard.update_dashboard(dashboard={'dashboard': {...}, 'folderId': 0, 'overwrite': True})

# Delete a dashboard by UID
grafana.dashboard.delete_dashboard(dashboard_uid='abcdefgh')

# Create organization
grafana.organization.create_organization({"name": "new_organization"})
```


## Authentication

There are two ways to authenticate to the Grafana API. Either use an API token,
or HTTP basic auth.

To use the admin API, you need to use HTTP basic auth, as stated at the
[Grafana Admin API documentation].

```python
from grafana_client import GrafanaApi

# Use HTTP basic authentication
grafana = GrafanaApi(
    auth=("username", "password"),
    host='grafana.example.org'
)

# Use Grafana API token
grafana = GrafanaApi(
    auth='eyJrIjoiWHg...dGJpZCI6MX0=',
    host='grafana.example.org'
)
```


## Status

This table outlines which parts of Grafana's HTTP API are covered by
`grafana-client`, see also [Grafana HTTP API reference].


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
| Health | + |
| Organisation | + |
| Other | + |
| Preferences | + |
| Snapshot | + |
| Teams | + |
| User | + |


## Software tests

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --editable=.[test]
python -m unittest -vvv
```


## Acknowledgements

Thanks to all the [contributors] who helped to co-create and conceive this
software in one way or another. You know who you are.


## Contributing

Any kind of contribution and feedback are very much welcome! Just create an
issue or submit a patch if you think we should include a new feature, or to 
report or fix a bug.

The issue tracker URL is: https://github.com/panodata/grafana-client/issues


## License

`grafana-client` is licensed under the terms of the MIT License, see [LICENSE] file.


[Andrew Prokhorenkov]: https://github.com/m0nhawk/grafana_api
[contributors]: https://github.com/panodata/grafana-client/graphs/contributors
[future maintenance of `grafana_api`]: https://github.com/m0nhawk/grafana_api/issues/88
[grafana_api]: https://github.com/m0nhawk/grafana_api
[Grafana Admin API documentation]: https://grafana.com/docs/grafana/latest/http_api/admin/
[Grafana HTTP API reference]: https://grafana.com/docs/grafana/latest/http_api/
[LICENSE]: https://github.com/panodata/grafana-client/blob/main/LICENSE
