import json

from loguru import logger
from mcp.server.fastmcp import FastMCP

from source.client import FlowerClient


def register(mcp: FastMCP, client: FlowerClient) -> None:
    @mcp.tool()
    async def get_queue_lengths() -> str:
        """Get the current length of all Celery queues."""
        data = await client.get("/api/queues/length")
        logger.info("Fetched queue lengths")
        return json.dumps(data)

    @mcp.tool()
    async def healthcheck() -> str:
        """Check whether the Flower instance is healthy."""
        data = await client.get("/healthcheck")
        logger.info("Healthcheck OK")
        return json.dumps(data)
