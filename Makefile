.PHONY: lint fmt typecheck test cov all

lint:
	uv run ruff check source/

fmt:
	uv run ruff format source/

typecheck:
	uv run mypy source/

test:
	uv run pytest tests/ -v

cov:
	uv run pytest tests/ --cov=source --cov-report=term-missing

all: fmt lint typecheck
