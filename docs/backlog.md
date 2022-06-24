# Backlog of grafana-client

## Iteration +1
- [o] Data source health check: Add more data source types.
  - loki, tempo, mssql, jaeger, zipkin
- [o] Community cherry-picking, see below.
- [o] Documentation
- [o] Release
- [o] Announcement on https://community.grafana.com/
- [o] Announcement at grafanalib

## Iteration +2
- [o] Unlock real data queries
  - See https://github.com/panodata/grafana-client/pull/5 ff.
  - [x] Provide initial example program for querying data sources
  - [o] Make example program `datasource-query.py` fully work
- [o] Use `grafana-wtf` to do the data source health check scan
  on a whole instance, instead of the example program here.

## Community contributions
- [o] Alerts
  - https://github.com/stephenlclarke/grafana_api/commit/606b58658e
- [o] Dashboard versions
  - https://github.com/DrMxxxxx/grafana_api/commit/fdf47a651be4
- [o] Query range and series
  - https://github.com/RalfHerzog/grafana_api/commit/57e1086a7
  - https://github.com/RalfHerzog/grafana_api/commit/68d505e
