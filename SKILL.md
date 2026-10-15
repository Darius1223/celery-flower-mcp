---
name: celery-flower
description: Monitor and control Celery via the celery-flower-mcp server — list workers and tasks, check queue depths, revoke or retry tasks, resize worker pools. Use when the user asks about Celery workers, tasks, queues, Flower, "why is the queue growing", "restart the worker", "what tasks are stuck".
---

# Celery / Flower control

Requires the `celery-flower-mcp` MCP server connected to a running Flower instance.
Setup: https://github.com/Darius1223/celery-flower-mcp#quick-start

## Start with a read

1. `healthcheck` — if it fails, stop and report; nothing else will work.
2. `list_workers` — who is alive, pool sizes, active task counts.
3. `get_queue_lengths` — where the backlog is.
4. `list_tasks` with `state=` (`STARTED`, `FAILURE`, `RETRY`) to narrow down.

## Common questions

| User asks | Do |
|---|---|
| "why is X slow / queue growing" | `get_queue_lengths` → `list_workers` → check which worker consumes that queue; suggest `grow_worker_pool` or `add_queue_consumer` |
| "what failed recently" | `list_tasks` with `state=FAILURE` and a date range, then `get_task_info` on the suspicious ones |
| "is task <uuid> done" | `get_task_info`, then `get_task_result` |
| "kill / cancel task" | `revoke_task` (with `terminate=true` only if the user confirms) |
| "run task Y" | `send_task` by name; use `apply_task` only when the user wants to wait for the result |
| "restart the worker" | `restart_worker_pool`, not `shutdown_worker` |

## Rules

- Always run a read tool before any write tool and show the user what you found.
- Destructive tools need explicit confirmation: `shutdown_worker`, `revoke_task` with terminate, `shrink_worker_pool`, `cancel_queue_consumer`.
- `abort_task` works only for tasks using `AbortableTask`; fall back to `revoke_task`.
- `set_task_rate_limit` format is Celery-style: `100/m`, `10/s`, `1000/h`.
- Flower reports what it has seen since start; a worker missing from `list_workers` may still be running. Say so instead of declaring it dead.
