.PHONY: format
format:
	.venv/bin/pip --quiet install black isort
	black grafana_client test examples
	isort grafana_client test examples

.PHONY: test
test:
	python -m unittest -vvv
