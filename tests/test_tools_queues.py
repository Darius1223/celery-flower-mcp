from unittest.mock import AsyncMock

import pytest
from mcp.server.fastmcp import FastMCP

from source.tools import queues


@pytest.fixture
def registered(mcp: FastMCP, mock_client: AsyncMock) -> FastMCP:
    queues.register(mcp, mock_client)
    return mcp


async def run(mcp: FastMCP, name: str, **kwargs: object) -> object:
    tool = mcp._tool_manager.get_tool(name)
    return await tool.run(kwargs, {})


async def test_get_queue_lengths(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"celery": 5, "high": 0}
    result = await run(registered, "get_queue_lengths")
    mock_client.get.assert_called_once_with("/api/queues/length")
    assert "celery" in str(result)


async def test_healthcheck(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"status": "ok"}
    result = await run(registered, "healthcheck")
    mock_client.get.assert_called_once_with("/healthcheck")
    assert "ok" in str(result)
