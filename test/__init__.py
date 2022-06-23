import os

# Purge environment variables to prevent them leaking from the user environment
# into the test suite.
PURGE_ENV_VARS = ["GRAFANA_URL", "GRAFANA_TOKEN"]

for envvar in PURGE_ENV_VARS:
    if envvar in os.environ:
        del os.environ[envvar]
