import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_async_container
from loguru import logger
from mcp.server.fastmcp import FastMCP

from source.client import FlowerClient
from source.providers import AppProvider
from source.tools import queues, tasks, workers

logger.remove()
logger.add(sys.stderr, level="INFO")

container = make_async_container(AppProvider())


@asynccontextmanager
async def lifespan(mcp: FastMCP) -> AsyncIterator[dict[str, object]]:
    client = await container.get(FlowerClient)
    logger.info("FlowerClient initialised")
    workers.register(mcp, client)
    tasks.register(mcp, client)
    queues.register(mcp, client)
    yield {}
    await container.close()
    logger.info("FlowerClient closed")


mcp = FastMCP("celery-flower", lifespan=lifespan)


if __name__ == "__main__":
    mcp.run()
