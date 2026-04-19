import json
from typing import Annotated

from loguru import logger
from mcp.server.fastmcp import FastMCP

from source.client import FlowerClient


def register(mcp: FastMCP, client: FlowerClient) -> None:  # noqa: PLR0915
    @mcp.tool()
    async def list_workers(
        refresh: Annotated[bool, "Run inspect to get updated worker list"] = False,
        workername: Annotated[str | None, "Filter to a specific worker name"] = None,
        status: Annotated[bool, "Return only alive/dead status per worker"] = False,
    ) -> str:
        """List all Celery workers."""
        params = {"refresh": refresh, "status": status}
        if workername:
            params["workername"] = workername  # type: ignore[assignment]
        data = await client.get("/api/workers", params=params)
        logger.info("Listed {} worker(s)", len(data) if isinstance(data, dict) else "?")
        return json.dumps(data)

    @mcp.tool()
    async def shutdown_worker(
        workername: Annotated[str, "Worker name, e.g. celery@worker1"],
    ) -> str:
        """Shut down a Celery worker."""
        data = await client.post(f"/api/worker/shutdown/{workername}")
        logger.info("Shutdown worker {}", workername)
        return json.dumps(data)

    @mcp.tool()
    async def restart_worker_pool(
        workername: Annotated[str, "Worker name"],
    ) -> str:
        """Restart a worker's process pool."""
        data = await client.post(f"/api/worker/pool/restart/{workername}")
        logger.info("Restarted pool for {}", workername)
        return json.dumps(data)

    @mcp.tool()
    async def grow_worker_pool(
        workername: Annotated[str, "Worker name"],
        n: Annotated[int, "Number of processes to add"] = 1,
    ) -> str:
        """Grow a worker's process pool by n processes."""
        data = await client.post(f"/api/worker/pool/grow/{workername}", params={"n": n})
        logger.info("Grew pool of {} by {}", workername, n)
        return json.dumps(data)

    @mcp.tool()
    async def shrink_worker_pool(
        workername: Annotated[str, "Worker name"],
        n: Annotated[int, "Number of processes to remove"] = 1,
    ) -> str:
        """Shrink a worker's process pool by n processes."""
        data = await client.post(f"/api/worker/pool/shrink/{workername}", params={"n": n})
        logger.info("Shrunk pool of {} by {}", workername, n)
        return json.dumps(data)

    @mcp.tool()
    async def autoscale_worker_pool(
        workername: Annotated[str, "Worker name"],
        min: Annotated[int, "Minimum number of pool processes"],
        max: Annotated[int, "Maximum number of pool processes"],
    ) -> str:
        """Set autoscale bounds for a worker's pool."""
        data = await client.post(
            f"/api/worker/pool/autoscale/{workername}",
            params={"min": min, "max": max},
        )
        logger.info("Autoscale {}: min={} max={}", workername, min, max)
        return json.dumps(data)

    @mcp.tool()
    async def add_queue_consumer(
        workername: Annotated[str, "Worker name"],
        queue: Annotated[str, "Queue name to start consuming from"],
    ) -> str:
        """Make a worker start consuming from a queue."""
        data = await client.post(
            f"/api/worker/queue/add-consumer/{workername}",
            params={"queue": queue},
        )
        logger.info("Worker {} now consuming from {}", workername, queue)
        return json.dumps(data)

    @mcp.tool()
    async def cancel_queue_consumer(
        workername: Annotated[str, "Worker name"],
        queue: Annotated[str, "Queue name to stop consuming from"],
    ) -> str:
        """Make a worker stop consuming from a queue."""
        data = await client.post(
            f"/api/worker/queue/cancel-consumer/{workername}",
            params={"queue": queue},
        )
        logger.info("Worker {} stopped consuming from {}", workername, queue)
        return json.dumps(data)
