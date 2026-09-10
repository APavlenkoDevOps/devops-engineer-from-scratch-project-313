run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8080

test:
	uv run pytest

lint:
	uv run ruff check .

check: lint test