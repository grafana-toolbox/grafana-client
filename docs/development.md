# Grafana Client development

## Sandbox
In order to create a development sandbox, you may want to follow this list of
commands. When you see the software tests succeed, you should be ready to start
hacking.

```shell
git clone https://github.com/panodata/grafana-client
cd grafana-client
python3 -m venv .venv
source .venv/bin/activate
pip install --editable=.[test,develop]

# Run all tests.
poe test

# Run specific tests.
python -m unittest -k preference -vvv
```

### Formatting

Before creating a PR, you can run `poe format`, in order to resolve code style issues.

## Run Grafana
```
docker run --rm -it --publish=3000:3000 --env='GF_SECURITY_ADMIN_PASSWORD=admin' grafana/grafana:9.3.6
```
