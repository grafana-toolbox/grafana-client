format:
	.venv/bin/pip --quiet install black isort
	black grafana_client test
	isort grafana_client test
