# Required for editable installs
# https://discuss.python.org/t/specification-of-editable-installation/1564/
from setuptools import setup

setup(
    name="grafana-client",
    use_scm_version={
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
        "write_to": "grafana_client/version.py",
    },
)
