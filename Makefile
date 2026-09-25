.PHONY: dev lint test check

FRAMEWORK ?= fastapi

dev:
	npx concurrently "uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload" "npx start-hexlet-devops-deploy-crud-frontend"

lint:
	uv run ruff check .

test:
	uv run pytest

check: lint test