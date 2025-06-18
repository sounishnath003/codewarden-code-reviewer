
.PHONY: fmt
fmt:
	uv run black .

.PHONY: install
install:
	uv add google-generativeai google-cloud-bigquery crewai black

.PHONY: run
run: fmt
	uv run main.py