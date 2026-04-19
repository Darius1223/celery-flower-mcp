.PHONY: lint fmt typecheck test cov integration integration-down all

lint:
	uv run ruff check source/

fmt:
	uv run ruff format source/

typecheck:
	uv run mypy source/

test:
	uv run pytest tests/ -v -m "not integration"

cov:
	uv run pytest tests/ --cov=source --cov-report=term-missing -m "not integration"

integration:
	docker compose -f docker-compose.test.yml up -d --build
	uv run pytest tests/integration/ -v --timeout=120
	docker compose -f docker-compose.test.yml down

integration-down:
	docker compose -f docker-compose.test.yml down -v

all: fmt lint typecheck
