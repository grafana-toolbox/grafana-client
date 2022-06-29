# Backlog of grafana-client

## Iteration +1
- [o] Community cherry-picking, see below.
- [o] Documentation
- [o] Release
- [o] Announcement on https://community.grafana.com/
- [o] Share `examples/grafanalib-upload-dashboard.py` with people at `grafanalib`

## Iteration +2
- [o] Unlock real data queries
  - See https://github.com/panodata/grafana-client/pull/5 ff.
  - Provide initial example program for querying data sources
  - Make example program `datasource-query.py` fully work
- [o] Use `grafana-wtf` to do the data source health check scan
  on a whole instance, instead of `examples/datasource-health-check.py`.
- [o] Spawn Grafana instance without authentication?
  - https://github.com/joe-elliott/tempo-otel-example/blob/master/docker-compose.yaml#L42-L44

## Community contributions
- [o] Alerts
  - https://github.com/stephenlclarke/grafana_api/commit/606b58658e
- [o] Dashboard versions
  - https://github.com/DrMxxxxx/grafana_api/commit/fdf47a651be4
- [o] Query range and series
  - https://github.com/RalfHerzog/grafana_api/commit/57e1086a7
  - https://github.com/RalfHerzog/grafana_api/commit/68d505e
- [o] Test mocks
  - https://github.com/m0nhawk/grafana_api/commit/21104835
- [o] Poetry
  - https://github.com/m0nhawk/grafana_api/commit/c3c4e686
