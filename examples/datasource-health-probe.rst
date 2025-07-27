################################
Grafana data source health probe
################################


*****
About
*****

``datasource-health-probe.py`` is an example program which can be used to
explore the data source health check feature on your local workstation, with
both Grafana and database service instances started using Docker.

Data source items are created on demand, so this program needs corresponding
permissions on the Grafana API to create and delete data source items.

The created data source items will be called ``probe-{type}``. For example,
``probe-prometheus``. After probing them, they will be deleted again.


*****
Setup
*****

Start Grafana::

    export GRAFANA_VERSION=7.5.16
    export GRAFANA_VERSION=8.5.6
    export GRAFANA_VERSION=9.0.2
    export GRAFANA_VERSION=main

    docker run --rm -it \
        --publish=3000:3000 \
        --env='GF_SECURITY_ADMIN_PASSWORD=admin' \
        grafana/grafana:${GRAFANA_VERSION}

In another shell, acquire the sources of this repository, and activate the
development sandbox::

    git clone https://github.com/grafana-toolbox/grafana-client
    cd grafana-client
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.[test]

The default Grafana URL is ``http://localhost:3000``, with credentials ``admin:admin``.
When needing to adjust that, use those environment variables::

    # Authenticate with credentials.
    export GRAFANA_URL=https://foo:bar@daq.example.com/grafana

    # Authenticate with token.
    export GRAFANA_URL=https://daq.example.com/grafana
    export GRAFANA_TOKEN=eyJrIjoiUWVrYXJh....aWQiOjJ9  # grafana-client-dev


*****
Usage
*****


Introduction
============

You will need two shells, a separate one for launching individual database
services with Docker, and the previous one where you just activated the
virtualenv of the developer sandbox and eventually adjusted the environment
variables.

In the next section, you will find instructions for running a data source
health check probe on different types of databases. When expanding this list,
please keep its items alphanumerically sorted.


CrateDB
=======
::

    docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate:4.8.1
    python examples/datasource-health-probe.py --type=cratedb --url=host.docker.internal:5432


Elasticsearch
=============
::

    # Start Elasticsearch.
    docker run --rm -it --publish=9200:9200 --env="discovery.type=single-node" \
        docker.elastic.co/elasticsearch/elasticsearch:7.17.4

    # Submit a data point. This automatically creates an index named `testdrive`.
    {apt,brew} install httpie
    http POST "http://localhost:9200/testdrive/_doc/1?pretty" "\@timestamp=2022-06-20T16:04:22.396Z" "sensor=foobar-1" "value=42.42"

    python examples/datasource-health-probe.py --type=elasticsearch --url=http://host.docker.internal:9200


Graphite
========
::

    docker run --rm -it --publish=8080:8080 graphiteapp/graphite-statsd:latest
    python examples/datasource-health-probe.py --type=graphite --url=http://host.docker.internal:8080


InfluxDB 1.x
============
::

    docker run --rm -it --publish=8086:8086 influxdb:1.8
    docker run --rm -it --network=host influxdb:1.8 influx -host host.docker.internal
    python examples/datasource-health-probe.py --type=influxdb --url=http://host.docker.internal:8086


InfluxDB 2.x
============
::

    # https://docs.influxdata.com/influxdb/v2.0/upgrade/v1-to-v2/docker/#influxdb-2x-initialization-credentials
    docker run --rm -it --publish=8086:8086 \
        --env=DOCKER_INFLUXDB_INIT_MODE=setup \
        --env=DOCKER_INFLUXDB_INIT_USERNAME=admin \
        --env=DOCKER_INFLUXDB_INIT_PASSWORD=adminadmin \
        --env=DOCKER_INFLUXDB_INIT_ORG=example \
        --env=DOCKER_INFLUXDB_INIT_BUCKET=default \
        --env=DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=admintoken \
        influxdb:2.2
    python examples/datasource-health-probe.py --type=influxdb+flux --url=http://host.docker.internal:8086

    docker run --rm -it --network=host influxdb:2.2 influx org list --token=admintoken
    docker run --rm -it --network=host influxdb:2.2 influx bucket list --org=example --token=admintoken

    export INFLUX_TOKEN=admintoken
    influx bucket list --org=example


Jaeger
======
::

    docker run --rm -it --name=jaeger --publish=16686:16686 jaegertracing/all-in-one:1
    python examples/datasource-health-probe.py --type=jaeger --url=http://host.docker.internal:16686


Loki
====
::

    docker run --rm -it --name=loki --publish=3100:3100 grafana/loki:2.5.0
    python examples/datasource-health-probe.py --type=loki --url=http://host.docker.internal:3100

MariaDB / MySQL
===============
::

    docker run --rm -it --publish=3306:3306 --env "MARIADB_ROOT_PASSWORD=root" mariadb:10
    python examples/datasource-health-probe.py --type=mysql --url=host.docker.internal:3306


Microsoft SQL Server
====================
::

    # Start service.
    docker run --rm -it --publish=1433:1433 \
        --env="ACCEPT_EULA=Y" --env="SA_PASSWORD=root123?" \
        mcr.microsoft.com/mssql/server:2022-latest

    # Create database `testdrive`.
    docker run --rm -it --network=host mcr.microsoft.com/mssql/server:2022-latest /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "root123?" -Q "CREATE DATABASE testdrive;"

    # Invoke Grafana database probe.
    python examples/datasource-health-probe.py --type=mssql --url=host.docker.internal:1433

Interactive client console::

    docker run --rm -it --network=host mcr.microsoft.com/mssql/server:2022-latest /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P root123?


OpenTSDB
========
::

    docker run --rm -it --publish=4242:4242 petergrace/opentsdb-docker:latest
    python examples/datasource-health-probe.py --type=opentsdb --url=host.docker.internal:4242


PostgreSQL
==========
::

    docker run --rm -it --publish=5432:5432 --env "POSTGRES_HOST_AUTH_METHOD=trust" postgres:14.3
    python examples/datasource-health-probe.py --type=postgres --url=host.docker.internal:5432


Prometheus
==========
::

    docker run --rm -it --publish=9090:9090 prom/prometheus
    python examples/datasource-health-probe.py --type=prometheus --url=http://host.docker.internal:9090


Tempo
=====
::

    docker run --rm -it --name=tempo --publish=3200:80 grafana/tempo:1.4.1 \
        --target=all --storage.trace.backend=local --storage.trace.local.path=/var/tempo --auth.enabled=false
    python examples/datasource-health-probe.py --type=tempo --url=http://host.docker.internal:3200


Testdata
========
::

    python examples/datasource-health-probe.py --type=testdata


Zipkin
======
::

    docker run --rm -it --publish=9411:9411 openzipkin/zipkin:2.23
    python examples/datasource-health-probe.py --type=zipkin --url=http://host.docker.internal:9411
