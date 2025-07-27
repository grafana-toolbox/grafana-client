# Backlog of grafana-client

## Iteration +1
- [x] Release 3.0.0
- [x] Announcement on https://community.grafana.com/
- [o] Share `examples/grafanalib-upload-dashboard.py` with people at `grafanalib`
- [o] Propagate features to `grafana-wtf`
- [o] Improve error output on `404 Not found`. See https://github.com/grafana-toolbox/grafana-client/issues/72
- [o] Add example using `grafana-dashboard`
  https://pypi.org/project/grafana-dashboard/

## Iteration +2
- [o] Unlock real data queries
  - See https://github.com/grafana-toolbox/grafana-client/pull/5 ff.
  - Provide initial example program for querying data sources
  - Make example program `datasource-query.py` fully work
- [o] Use `grafana-wtf` to do the data source health check scan
  on a whole instance, instead of `examples/datasource-health-check.py`.
- [o] Spawn Grafana instance without authentication?
  - https://github.com/joe-elliott/tempo-otel-example/blob/master/docker-compose.yaml#L42-L44
- [o] The old & new alerting API
- [o] Community cherry-picking, see below.

## Iteration +3
- [o] Add support for more data source health checks
  - https://github.com/yesoreyeram/grafana-infinity-datasource
  - https://github.com/scottlepp/grafana-sqlproxy-datasource
  - https://github.com/grafana/mqtt-datasource
  - https://github.com/grafana/google-bigquery-datasource
  - https://github.com/orgs/grafana/repositories?q=datasource
  - https://github.com/search?q=grafana+datasource

## Community contributions
- [o] Alerts
  - https://github.com/stephenlclarke/grafana_api/commit/606b58658e
- [o] Test mocks
  - https://github.com/m0nhawk/grafana_api/commit/21104835
- [o] Poetry
  - https://github.com/m0nhawk/grafana_api/commit/c3c4e686
