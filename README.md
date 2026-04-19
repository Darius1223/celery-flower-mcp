# 🌸 celery-flower-mcp

<div align="center">

[![CI](https://github.com/Darius1223/celery-flower-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Darius1223/celery-flower-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Darius1223/celery-flower-mcp/graph/badge.svg)](https://codecov.io/gh/Darius1223/celery-flower-mcp)
[![PyPI](https://img.shields.io/pypi/v/celery-flower-mcp.svg)](https://pypi.org/project/celery-flower-mcp/)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Smithery](https://smithery.ai/badge/celery-flower-mcp)](https://smithery.ai/server/celery-flower-mcp)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Give your AI assistant full control over Celery — monitor workers, manage tasks, inspect queues.**

[Features](#features) · [Quick Start](#quick-start) · [Configuration](#configuration) · [Tools](#available-tools) · [Development](#development) · [Contributing](CONTRIBUTING.md)

</div>

---

## What is this?

`celery-flower-mcp` is a [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes the full [Celery Flower](https://flower.readthedocs.io/) REST API as MCP tools. Point it at your Flower instance and your AI assistant (Claude, Cursor, Windsurf, etc.) can:

- **Monitor** workers, tasks, and queues in real time
- **Control** worker pools — grow, shrink, autoscale, restart, shut down
- **Manage tasks** — apply, revoke, abort, set timeouts and rate limits
- **Inspect queues** — check depths, add/remove consumers

All 21 Flower API endpoints are covered.

## Features

- **Full API coverage** — every Flower REST endpoint exposed as an MCP tool
- **Dependency injection** via [dishka](https://dishka.readthedocs.io/) — clean, testable architecture
- **Pydantic Settings** — typed configuration with `.env` file support
- **Async** throughout — built on `httpx` + `FastMCP`
- **99% test coverage** — 49 tests, zero flakes
- **Strict typing** — mypy strict mode, fully annotated

## Quick Start

### Install via Smithery (recommended)

```bash
npx @smithery/cli install celery-flower-mcp --client claude
```

### Install via uvx

```bash
FLOWER_URL=http://localhost:5555 uvx celery-flower-mcp
```

### Install from source

```bash
git clone https://github.com/Darius1223/celery-flower-mcp
cd celery-flower-mcp
uv sync
uv run python -m source.main
```

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "celery-flower": {
      "command": "uvx",
      "args": ["celery-flower-mcp"],
      "env": {
        "FLOWER_URL": "http://localhost:5555"
      }
    }
  }
}
```

## Configuration

Configuration is read from environment variables or a `.env` file in the project root. Copy `.env.example` to get started:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `FLOWER_URL` | `http://localhost:5555` | Base URL of your Flower instance |
| `FLOWER_USERNAME` | — | Basic auth username |
| `FLOWER_PASSWORD` | — | Basic auth password |
| `FLOWER_API_TOKEN` | — | Bearer token (takes priority over basic auth) |

## Available Tools

### Workers (8 tools)

| Tool | Description |
|---|---|
| `list_workers` | List all workers — optionally filter by name, refresh live stats, or get status only |
| `shutdown_worker` | Gracefully shut down a worker |
| `restart_worker_pool` | Restart a worker's process pool |
| `grow_worker_pool` | Add N processes to a worker's pool |
| `shrink_worker_pool` | Remove N processes from a worker's pool |
| `autoscale_worker_pool` | Configure autoscale min/max bounds |
| `add_queue_consumer` | Make a worker start consuming from a queue |
| `cancel_queue_consumer` | Make a worker stop consuming from a queue |

### Tasks (11 tools)

| Tool | Description |
|---|---|
| `list_tasks` | List tasks with filters: state, worker, name, date range, search, pagination |
| `list_task_types` | List all registered task types across workers |
| `get_task_info` | Get full details for a task by UUID |
| `get_task_result` | Retrieve a task's result (with optional timeout) |
| `apply_task` | Execute a task synchronously and wait for the result |
| `async_apply_task` | Dispatch a task asynchronously, returns task UUID |
| `send_task` | Send a task by name — no registration required on worker side |
| `abort_task` | Abort a running task |
| `revoke_task` | Revoke a task; optionally terminate with a signal |
| `set_task_timeout` | Set soft and/or hard time limits for a task on a worker |
| `set_task_rate_limit` | Set rate limit for a task on a worker (e.g. `100/m`) |

### Queues & Health (2 tools)

| Tool | Description |
|---|---|
| `get_queue_lengths` | Get the current depth of all configured queues |
| `healthcheck` | Check whether the Flower instance is reachable and healthy |

## Architecture

```
source/
├── main.py        # FastMCP server entry point + dishka container wiring
├── settings.py    # Pydantic Settings — typed config from env / .env
├── client.py      # Async HTTP client wrapping Flower REST API
├── providers.py   # dishka Provider — manages FlowerClient lifecycle
└── tools/
    ├── workers.py # 8 worker management tools
    ├── tasks.py   # 11 task management tools
    └── queues.py  # 2 queue / health tools
```

[dishka](https://dishka.readthedocs.io/) manages the `FlowerClient` lifecycle: created once at startup, closed cleanly on shutdown via an async generator provider.

## Development

```bash
make fmt        # auto-format with ruff
make lint       # lint with ruff
make typecheck  # type-check with mypy (strict)
make test       # run 49 tests
make cov        # tests + coverage report
make all        # fmt + lint + typecheck
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new tools or submitting a PR.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
