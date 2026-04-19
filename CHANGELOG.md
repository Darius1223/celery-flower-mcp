# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-04-19

### Added
- Integration test suite (16 tests) against a real Flower + Redis + Celery worker stack via Docker Compose
- `docker-compose.test.yml` with Redis, worker, and Flower services including healthchecks
- `make integration` / `make integration-down` Makefile targets
- CI: integration test job with container log dump on failure

### Fixed
- Task apply endpoints (`apply_task`, `async_apply_task`, `send_task`) now send JSON body instead of form-data — required by Flower 2.0
- `list_workers` now passes `refresh=True` to get live worker state from Flower
- Integration tests use `pytest.mark.asyncio(loop_scope="session")` to share one event loop, preventing `RuntimeError: Event loop is closed` on Python 3.14

## [0.1.0] - 2026-04-18

### Added
- Full coverage of the Celery Flower REST API — 21 MCP tools across workers, tasks, and queues
- Async HTTP client via `httpx`
- Dependency injection via `dishka` with proper `APP`-scoped lifecycle management
- Typed configuration via `pydantic-settings` with `.env` file support
- Basic auth and bearer token authentication
- 99% test coverage (49 tests) with `pytest-asyncio` and `pytest-httpx`
- Strict type checking with `mypy`
- Code quality with `ruff` (lint + format)
- GitHub Actions CI (lint, typecheck, test + Codecov upload)
