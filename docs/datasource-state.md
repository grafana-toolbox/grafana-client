# Data source health check - state of the onion


## play.grafana.org

### OK
```
fetzerch-sunandmoon-datasource
grafana-bigquery-datasource
grafana-iot-sitewise-datasource
grafana-iot-twinmaker-datasource
grafana-github-datasource
grafana-googlesheets-datasource
graphite
influxdb  # 1.x and 2.x
mysql
postgres
prometheus
stackdriver
testdata
```

### UNKNOWN

### TODO
```
alertmanager
cognitedata-datasource
fetzerch-sunandmoon-datasource
grafana-cardinality-datasource
grafana-doom-datasource
marcusolsson-static-datasource
```

### VALIDATE
```
cloudwatch
```


## weather.hiveeyes.org

### OK
```
fetzerch-sunandmoon-datasource
influxdb  # 1.x
postgres
```

### ERROR
```
fetzerch-sunandmoon-datasource
grafana-simple-json-datasource
postgres
simpod-json-datasource
```

### UNKNOWN
```
goshposh-metaqueries-datasource
grafana-influxdb-flux-datasource
```
