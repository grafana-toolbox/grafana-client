# grafana-client

[![Tests](https://github.com/grafana-toolbox/grafana-client/workflows/Test/badge.svg)](https://github.com/grafana-toolbox/grafana-client/actions?query=workflow%3ATest)
[![Test coverage](https://img.shields.io/codecov/c/gh/grafana-toolbox/grafana-client.svg?style=flat-square)](https://codecov.io/gh/grafana-toolbox/grafana-client/)
[![License](https://img.shields.io/github/license/grafana-toolbox/grafana-client.svg?style=flat-square)](https://github.com/grafana-toolbox/grafana-client/blob/main/LICENSE)

[![Python versions](https://img.shields.io/pypi/pyversions/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![Grafana versions](https://img.shields.io/badge/Grafana-5.x%20--%2011.x-blue.svg?style=flat-square)](https://github.com/grafana/grafana)

[![Status](https://img.shields.io/pypi/status/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![PyPI](https://img.shields.io/pypi/v/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
[![Downloads](https://img.shields.io/pypi/dm/grafana-client.svg?style=flat-square)](https://pypi.org/project/grafana-client/)
<!-- [![Conda](https://img.shields.io/conda/v/grafana-toolbox/grafana-client.svg?style=flat-square)](https://anaconda.org/grafana-toolbox/grafana-client) -->


## About

A client library for accessing the Grafana HTTP API, written in Python.


## Setup

Install the package from PyPI.
```
pip install --upgrade grafana-client
```


## Usage

### API overview

This section gives you an idea about how to use the API on behalf of a few
samples.

#### Synchronous
```python
from grafana_client import GrafanaApi

# Connect to Grafana API endpoint using the `GrafanaApi` class
grafana = GrafanaApi.from_url(
    "https://username:password@daq.example.org/grafana/")

# Create user
user = grafana.admin.create_user({
    "name": "User",
    "email": "user@example.org",
    "login": "user",
    "password": "userpassword",
    "OrgId": 1,
})

# Change user password
user = grafana.admin.change_user_password(2, "newpassword")

# Search dashboards based on tag
grafana.search.search_dashboards(tag="applications")

# Find a user by email
user = grafana.users.find_user("test@example.org")

# Add user to team 2
grafana.teams.add_team_member(2, user["id"])

# Create or update a dashboard
grafana.dashboard.update_dashboard(
    dashboard={"dashboard": {...}, "folderId": 0, "overwrite": True})

# Delete a dashboard by UID
grafana.dashboard.delete_dashboard(dashboard_uid="foobar")

# Create organization
grafana.organization.create_organization(
    organization={"name": "new_organization"})
```

#### Asynchronous

The asynchronous interfaces are identical, except for the fact that you will
need to properly handle coroutines (async/await).

```python
import asyncio
from grafana_client import AsyncGrafanaApi

async def main():
    # Connect to Grafana API endpoint using the `GrafanaApi` class
    grafana = AsyncGrafanaApi.from_url("https://username:password@daq.example.org/grafana/")

    # Create user
    user = await grafana.admin.create_user({
        "name": "User",
        "email": "user@example.org",
        "login": "user",
        "password": "userpassword",
        "OrgId": 1,
    })

    # Change user password
    user = await grafana.admin.change_user_password(2, "newpassword")

asyncio.run(main())
```

### Example programs

There are complete example programs to get you started within the [examples
folder] of this repository.

Feel free to use them as blueprints for your own programs. If you think your
exercises could be useful for others, don't hesitate to share them back.


## Configuration Settings

### Authentication

There are several ways to authenticate to the Grafana HTTP API.

1. Anonymous access
2. Grafana API token
3. HTTP Basic Authentication
4. HTTP Header Authentication

The [Grafana Admin API] is a subset of the Grafana API. For accessing those API
resources, you will need to use HTTP Basic Authentication.

```python
from grafana_client import GrafanaApi, HeaderAuth, TokenAuth

# 1. Anonymous access
grafana = GrafanaApi.from_url(
    url="https://daq.example.org/grafana/",
)

# 2. Use Grafana API token.
grafana = GrafanaApi.from_url(
    url="https://daq.example.org/grafana/",
    credential=TokenAuth(token="eyJrIjoiWHg...dGJpZCI6MX0="),
)

# 3. Use HTTP basic authentication.
grafana = GrafanaApi.from_url(
    url="https://username:password@daq.example.org/grafana/",
)
grafana = GrafanaApi.from_url(
    url="https://daq.example.org/grafana/",
    credential=("username", "password")
)

# 4. Use HTTP Header authentication.
grafana = GrafanaApi.from_url(
    url="https://daq.example.org/grafana/",
    credential=HeaderAuth(name="X-WEBAUTH-USER", value="foobar"),
)

# Optionally turn off TLS certificate verification.
grafana = GrafanaApi.from_url(
    url="https://username:password@daq.example.org/grafana/?verify=false",
)

# Use `GRAFANA_URL` and `GRAFANA_TOKEN` environment variables.
grafana = GrafanaApi.from_env()
```

Please note that, on top of the specific examples above, the object obtained by
`credential` can be an arbitrary `niquests.auth.AuthBase` instance.

### DNS Resolver

`niquests` support using a custom DNS resolver, like but not limited, DNS-over-HTTPS, and DNS-over-QUIC.
You will have to set `NIQUESTS_DNS_URL` environment variable. For example:
```
export NIQUESTS_DNS_URL="doh+cloudflare://"
```

See the [documentation](https://niquests.readthedocs.io/en/latest/user/quickstart.html#set-dns-via-environment) to learn
more about accepted URL parameters and protocols.

### Grafana Organization

If the Grafana API is authenticated as a user (for example, with HTTP Basic Authentication),
it will use the user's current organization context.
That context can be changed with the `GrafanaApi.user.switch_actual_user_organisation` function.

```python
grafana.user.switch_actual_user_organisation(1)
```

An instance of `GrafanaApi` can also be bound to a single organization with the `organization_id` parameter,
ensuring that all requests will be made to that organization.
This parameter will cause `GrafanaClient` to use the [X-Grafana-Org-Id header].

```python
grafana = GrafanaApi(..., organization_id=1)
```

API Tokens are bound to a single organization, so the `organization_id` parameter does not need to be specified.

### HTTP Proxy

The underlying `niquests` library honors the `HTTP_PROXY` and `HTTPS_PROXY`
environment variables. Setting them before invoking an application using
`grafana-client` has been confirmed to work. For example:
```
export HTTP_PROXY=10.10.1.10:3128
export HTTPS_PROXY=10.10.1.11:1080
```

### Pool Size

By default a session pool size of 10 is used. This can be changed by passing
the `session_pool_size` argument to the `GrafanaApi` constructor:
```python
grafana.client.session_pool_size = 32
```

### TCP Timeout

The default timeout value is five seconds, used for both connect and read timeout.

The constructors of `GrafanaApi` and `GrafanaClient`, as well as the factory methods
`from_url` and `from_env` accept the `timeout` argument, which can be obtained as a
scalar `float` value, or as a tuple of `(<read timeout>, <connect timeout>)`.


## Details

This section of the documentation outlines which parts of the Grafana HTTP API
are supported, and to which degree. See also [Grafana HTTP API reference].

### Compatibility

`grafana-client` is largely compatible with Grafana 5.x-10.x. However, earlier
versions of Grafana might not support certain features or subsystems.

### Overview

| API | Status |
|---|---|
| Admin | + |
| Alerting | +- |
| Alerting Notification Channels | + |
| Alerting Provisioning | + |
| Annotations | + |
| Authentication | +- |
| Dashboard | + |
| Dashboard Versions | + |
| Dashboard Permissions | + |
| Data Source | + |
| Data Source Permissions | + |
| External Group Sync | + |
| Folder | + |
| Folder Permissions | + |
| Folder/Dashboard Search | +- |
| Health | + |
| Library Elements | + |
| Organisation | + |
| Other | + |
| Plugin | + |
| Preferences | + |
| Rbac | +- |
| Snapshot | + |
| Teams | + |
| User | + |


### Data source health check

#### Introduction

For checking whether a Grafana data source is healthy, Grafana 9 and newer has
a server-side data source health check API. For earlier versions, a client-side
implementation is provided.

This implementation works in the same manner as the "Save & test" button works,
when creating a data source in the user interface.

The feature can be explored through corresponding client programs in the
[examples folder] of this repository.

#### Compatibility

The minimum required version for data source health checks is Grafana 7.
Prometheus only works on Grafana 8 and newer.

#### Data source coverage

Health checks are supported for these Grafana data source types.

- CrateDB
- Elasticsearch
- Graphite
- InfluxDB
- Jaeger
- Loki
- Microsoft SQL Server
- OpenTSDB
- PostgreSQL
- Prometheus
- Tempo
- Testdata
- Zipkin

We are humbly asking the community to contribute adapters for other data
source types, popular or not.


## Applications

A list of applications based on `grafana-client`.

- [grafana-import-tool](https://github.com/peekjef72/grafana-import-tool)
- [grafana-ldap-sync-script](https://github.com/NovatecConsulting/grafana-ldap-sync-script)
- [grafana-snapshots-tool](https://github.com/peekjef72/grafana-snapshots-tool)
- [grafana-wtf](https://github.com/grafana-toolbox/grafana-wtf)
- [nixops-grafana](https://github.com/tewfik-ghariani/nixops-grafana)


## Project information

### History

The library was originally conceived by [Andrew Prokhorenkov] and contributors
as [grafana_api]. Thank you very much for your efforts!

At [future maintenance of `grafana_api`], we discussed the need for a fork
because the repository stopped receiving updates since more than a year.
While forking it, we renamed the package to `grafana-client` and slightly
trimmed the module namespace.


### Acknowledgements

Thanks to the original authors and all [contributors] who helped to co-create
and conceive this software in one way or another. You know who you are.


### Contributing

Any kind of contribution and feedback are very much welcome! Just create an
issue or submit a patch if you think we should include a new feature, or to
report or fix a bug.

The issue tracker URL is: https://github.com/grafana-toolbox/grafana-client/issues


### Development

In order to set up a development environment for `grafana-client`, please
follow the [development documentation].


### License

`grafana-client` is licensed under the terms of the MIT License, see [LICENSE] file.

### Supported by

[![JetBrains logo.](https://resources.jetbrains.com/storage/products/company/brand/logos/jetbrains.svg)](https://jb.gg/OpenSourceSupport)

Special thanks to the people at JetBrains s.r.o. for supporting us with
excellent development tooling.


[Andrew Prokhorenkov]: https://github.com/m0nhawk/grafana_api
[contributors]: https://github.com/grafana-toolbox/grafana-client/graphs/contributors
[development documentation]: https://github.com/grafana-toolbox/grafana-client/blob/main/docs/development.md
[examples folder]: https://github.com/grafana-toolbox/grafana-client/tree/main/examples
[future maintenance of `grafana_api`]: https://github.com/m0nhawk/grafana_api/issues/88
[grafana_api]: https://github.com/m0nhawk/grafana_api
[Grafana Admin API]: https://grafana.com/docs/grafana/latest/http_api/admin/
[X-Grafana-Org-Id header]: https://grafana.com/docs/grafana/latest/developers/http_api/auth/#x-grafana-org-id-header
[Grafana HTTP API reference]: https://grafana.com/docs/grafana/latest/http_api/
[LICENSE]: https://github.com/grafana-toolbox/grafana-client/blob/main/LICENSE
