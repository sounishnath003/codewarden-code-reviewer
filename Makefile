
.PHONY: fmt
fmt:
	uv run black .

.PHONY: install
install:
	uv add google-generativeai google-cloud-bigquery crewai black pyyaml

.PHONY: run
run: fmt
	find . -type d -name __pycache__ | xargs rm -fr 
	uv run main.py --config dev.config.yaml