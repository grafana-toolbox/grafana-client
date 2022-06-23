.PHONY: format
format:
	.venv/bin/pip --quiet install black isort
	black grafana_client test examples
	isort grafana_client test examples

.PHONY: test
test:
	python -m unittest -vvv

.PHONY: test-coverage
test-coverage:
	coverage run -m unittest -vvv
	coverage report
