# Grafana Client development

## Sandbox
In order to create a development sandbox, you may want to follow this list of
commands.
```shell
git clone https://github.com/grafana-toolbox/grafana-client
cd grafana-client
python3 -m venv .venv
source .venv/bin/activate
pip install --editable=.[test,develop]
```

## Software Tests
When you see the software tests succeed, you should be ready to start
hacking.
```shell
# Run linters and software tests.
poe check

# Run specific tests.
python -m unittest -vvv -k preference
```

## Code Formatting
Before submitting a PR, please format the code, in order to invoke the async
translation program and to resolve code style issues.
```shell
poe format
```

The async translation program populates the `grafana_client/elements/_async`
folder automatically. Please do not edit files there manually.

## Run Grafana
```
docker run --rm -it --publish=3000:3000 --env='GF_SECURITY_ADMIN_PASSWORD=admin' grafana/grafana:9.3.6
```
