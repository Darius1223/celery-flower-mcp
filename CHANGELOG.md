# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
