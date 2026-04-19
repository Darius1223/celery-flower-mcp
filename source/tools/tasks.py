import json
from typing import Annotated

from loguru import logger
from mcp.server.fastmcp import FastMCP

from source.client import FlowerClient


def register(mcp: FastMCP, client: FlowerClient) -> None:  # noqa: PLR0915
    @mcp.tool()
    async def list_tasks(
        limit: Annotated[int | None, "Maximum number of tasks to return"] = None,
        offset: Annotated[int | None, "Number of tasks to skip"] = None,
        workername: Annotated[str | None, "Filter by worker name"] = None,
        taskname: Annotated[str | None, "Filter by task name"] = None,
        state: Annotated[str | None, "Filter by state (SUCCESS, FAILURE, etc.)"] = None,
        received_start: Annotated[str | None, "Filter tasks received after this datetime"] = None,
        received_end: Annotated[str | None, "Filter tasks received before this datetime"] = None,
        sort_by: Annotated[str | None, "Field to sort by"] = None,
        search: Annotated[str | None, "Search string"] = None,
    ) -> str:
        """List tasks with optional filters."""
        params = {
            k: v
            for k, v in {
                "limit": limit,
                "offset": offset,
                "workername": workername,
                "taskname": taskname,
                "state": state,
                "received_start": received_start,
                "received_end": received_end,
                "sort_by": sort_by,
                "search": search,
            }.items()
            if v is not None
        }
        data = await client.get("/api/tasks", params=params)
        logger.info("Listed {} task(s)", len(data) if isinstance(data, dict) else "?")
        return json.dumps(data)

    @mcp.tool()
    async def list_task_types() -> str:
        """List all registered task types."""
        data = await client.get("/api/task/types")
        logger.info("Fetched task types")
        return json.dumps(data)

    @mcp.tool()
    async def get_task_info(
        task_id: Annotated[str, "Task UUID"],
    ) -> str:
        """Get detailed information about a task by its ID."""
        data = await client.get(f"/api/task/info/{task_id}")
        logger.info("Fetched info for task {}", task_id)
        return json.dumps(data)

    @mcp.tool()
    async def get_task_result(
        task_id: Annotated[str, "Task UUID"],
        timeout: Annotated[float | None, "Seconds to wait for result"] = None,
    ) -> str:
        """Get the result of a task."""
        params = {"timeout": timeout} if timeout is not None else None
        data = await client.get(f"/api/task/result/{task_id}", params=params)
        logger.info("Fetched result for task {}", task_id)
        return json.dumps(data)

    @mcp.tool()
    async def apply_task(
        taskname: Annotated[str, "Full task name, e.g. myapp.tasks.add"],
        args: Annotated[str | None, "JSON-encoded positional args list"] = None,
        kwargs: Annotated[str | None, "JSON-encoded keyword args dict"] = None,
        options: Annotated[str | None, "JSON-encoded apply options dict"] = None,
    ) -> str:
        """Execute a task synchronously and wait for the result."""
        data_dict = {
            k: v
            for k, v in {"args": args, "kwargs": kwargs, "options": options}.items()
            if v is not None
        }
        data = await client.post(f"/api/task/apply/{taskname}", data=data_dict)
        logger.info("Applied task {}", taskname)
        return json.dumps(data)

    @mcp.tool()
    async def async_apply_task(
        taskname: Annotated[str, "Full task name"],
        args: Annotated[str | None, "JSON-encoded positional args list"] = None,
        kwargs: Annotated[str | None, "JSON-encoded keyword args dict"] = None,
        options: Annotated[str | None, "JSON-encoded apply options dict"] = None,
    ) -> str:
        """Execute a task asynchronously and return its task ID."""
        data_dict = {
            k: v
            for k, v in {"args": args, "kwargs": kwargs, "options": options}.items()
            if v is not None
        }
        data = await client.post(f"/api/task/async-apply/{taskname}", data=data_dict)
        logger.info("Async-applied task {}", taskname)
        return json.dumps(data)

    @mcp.tool()
    async def send_task(
        taskname: Annotated[str, "Full task name"],
        args: Annotated[str | None, "JSON-encoded positional args list"] = None,
        kwargs: Annotated[str | None, "JSON-encoded keyword args dict"] = None,
        options: Annotated[str | None, "JSON-encoded send options dict"] = None,
    ) -> str:
        """Send a task via send_task (does not require task to be registered on the worker)."""
        data_dict = {
            k: v
            for k, v in {"args": args, "kwargs": kwargs, "options": options}.items()
            if v is not None
        }
        data = await client.post(f"/api/task/send-task/{taskname}", data=data_dict)
        logger.info("Sent task {}", taskname)
        return json.dumps(data)

    @mcp.tool()
    async def abort_task(
        task_id: Annotated[str, "Task UUID"],
    ) -> str:
        """Abort a running task."""
        data = await client.post(f"/api/task/abort/{task_id}")
        logger.info("Aborted task {}", task_id)
        return json.dumps(data)

    @mcp.tool()
    async def revoke_task(
        task_id: Annotated[str, "Task UUID"],
        terminate: Annotated[bool, "Terminate the task if it is already running"] = False,
        signal: Annotated[str, "Signal to send when terminating"] = "SIGTERM",
    ) -> str:
        """Revoke a task, optionally terminating it if running."""
        data = await client.post(
            f"/api/task/revoke/{task_id}",
            params={"terminate": terminate, "signal": signal},
        )
        logger.info("Revoked task {}", task_id)
        return json.dumps(data)

    @mcp.tool()
    async def set_task_timeout(
        taskname: Annotated[str, "Full task name"],
        workername: Annotated[str, "Worker name to apply the limit on"],
        soft: Annotated[float | None, "Soft time limit in seconds"] = None,
        hard: Annotated[float | None, "Hard time limit in seconds"] = None,
    ) -> str:
        """Change soft and hard time limits for a task on a worker."""
        params: dict[str, str] = {"workername": workername}
        if soft is not None:
            params["soft"] = str(soft)
        if hard is not None:
            params["hard"] = str(hard)
        data = await client.post(f"/api/task/timeout/{taskname}", params=params)
        logger.info("Set timeout for task {} on {}", taskname, workername)
        return json.dumps(data)

    @mcp.tool()
    async def set_task_rate_limit(
        taskname: Annotated[str, "Full task name"],
        workername: Annotated[str, "Worker name to apply the rate limit on"],
        ratelimit: Annotated[str, "Rate limit value, e.g. '100/m'"],
    ) -> str:
        """Change the rate limit for a task on a worker."""
        data = await client.post(
            f"/api/task/rate-limit/{taskname}",
            params={"workername": workername, "ratelimit": ratelimit},
        )
        logger.info("Set rate limit for task {} on {}: {}", taskname, workername, ratelimit)
        return json.dumps(data)
