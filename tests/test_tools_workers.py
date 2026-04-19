import json
from unittest.mock import AsyncMock

import pytest
from mcp.server.fastmcp import FastMCP

from source.tools import workers


@pytest.fixture
def registered(mcp: FastMCP, mock_client: AsyncMock) -> FastMCP:
    workers.register(mcp, mock_client)
    return mcp


async def run(mcp: FastMCP, name: str, **kwargs: object) -> object:
    tool = mcp._tool_manager.get_tool(name)
    return await tool.run(kwargs, {})


async def test_list_workers_default(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"celery@w1": {}}
    result = await run(registered, "list_workers")
    mock_client.get.assert_called_once_with(
        "/api/workers", params={"refresh": False, "status": False}
    )
    assert json.loads(str(result)) == {"celery@w1": {}}


async def test_list_workers_with_name(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {}
    await run(registered, "list_workers", workername="celery@w1", refresh=True, status=True)
    call_params = mock_client.get.call_args[1]["params"]
    assert call_params["workername"] == "celery@w1"
    assert call_params["refresh"] is True
    assert call_params["status"] is True


async def test_shutdown_worker(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.post.return_value = {"message": "Shutting down!"}
    result = await run(registered, "shutdown_worker", workername="celery@w1")
    mock_client.post.assert_called_once_with("/api/worker/shutdown/celery@w1")
    assert "Shutting down!" in str(result)


async def test_restart_worker_pool(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "restart_worker_pool", workername="celery@w1")
    mock_client.post.assert_called_once_with("/api/worker/pool/restart/celery@w1")


async def test_grow_worker_pool(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "grow_worker_pool", workername="celery@w1", n=3)
    mock_client.post.assert_called_once_with(
        "/api/worker/pool/grow/celery@w1", params={"n": 3}
    )


async def test_grow_worker_pool_default_n(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "grow_worker_pool", workername="celery@w1")
    mock_client.post.assert_called_once_with(
        "/api/worker/pool/grow/celery@w1", params={"n": 1}
    )


async def test_shrink_worker_pool(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "shrink_worker_pool", workername="celery@w1", n=2)
    mock_client.post.assert_called_once_with(
        "/api/worker/pool/shrink/celery@w1", params={"n": 2}
    )


async def test_autoscale_worker_pool(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "autoscale_worker_pool", workername="celery@w1", min=2, max=10)
    mock_client.post.assert_called_once_with(
        "/api/worker/pool/autoscale/celery@w1", params={"min": 2, "max": 10}
    )


async def test_add_queue_consumer(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "add_queue_consumer", workername="celery@w1", queue="myqueue")
    mock_client.post.assert_called_once_with(
        "/api/worker/queue/add-consumer/celery@w1", params={"queue": "myqueue"}
    )


async def test_cancel_queue_consumer(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "cancel_queue_consumer", workername="celery@w1", queue="myqueue")
    mock_client.post.assert_called_once_with(
        "/api/worker/queue/cancel-consumer/celery@w1", params={"queue": "myqueue"}
    )
