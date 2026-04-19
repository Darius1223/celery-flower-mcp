import json
from unittest.mock import AsyncMock

import pytest
from mcp.server.fastmcp import FastMCP

from source.tools import tasks


@pytest.fixture
def registered(mcp: FastMCP, mock_client: AsyncMock) -> FastMCP:
    tasks.register(mcp, mock_client)
    return mcp


async def run(mcp: FastMCP, name: str, **kwargs: object) -> object:
    tool = mcp._tool_manager.get_tool(name)
    return await tool.run(kwargs, {})


async def test_list_tasks_no_filters(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"task1": {}}
    result = await run(registered, "list_tasks")
    mock_client.get.assert_called_once_with("/api/tasks", params={})
    assert "task1" in str(result)


async def test_list_tasks_with_filters(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {}
    await run(registered, "list_tasks", state="SUCCESS", limit=10, workername="celery@w1")
    params = mock_client.get.call_args[1]["params"]
    assert params["state"] == "SUCCESS"
    assert params["limit"] == 10
    assert params["workername"] == "celery@w1"
    assert "offset" not in params


async def test_list_tasks_all_filters(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {}
    await run(
        registered,
        "list_tasks",
        limit=5,
        offset=0,
        workername="celery@w1",
        taskname="my.task",
        state="FAILURE",
        received_start="2024-01-01",
        received_end="2024-12-31",
        sort_by="received",
        search="foo",
    )
    params = mock_client.get.call_args[1]["params"]
    assert len(params) == 9


async def test_list_task_types(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = ["my.task"]
    result = await run(registered, "list_task_types")
    mock_client.get.assert_called_once_with("/api/task/types")
    assert "my.task" in str(result)


async def test_get_task_info(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"id": "abc-123"}
    await run(registered, "get_task_info", task_id="abc-123")
    mock_client.get.assert_called_once_with("/api/task/info/abc-123")


async def test_get_task_result_no_timeout(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {"result": 42}
    await run(registered, "get_task_result", task_id="abc-123")
    mock_client.get.assert_called_once_with("/api/task/result/abc-123", params=None)


async def test_get_task_result_with_timeout(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.get.return_value = {}
    await run(registered, "get_task_result", task_id="abc-123", timeout=5.0)
    mock_client.get.assert_called_once_with(
        "/api/task/result/abc-123", params={"timeout": 5.0}
    )


async def test_apply_task_no_args(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "apply_task", taskname="my.task")
    mock_client.post.assert_called_once_with("/api/task/apply/my.task", json={})


async def test_apply_task_with_args(registered: FastMCP, mock_client: AsyncMock) -> None:
    # Pass non-JSON strings to avoid FastMCP pre-parsing
    await run(registered, "apply_task", taskname="my.task", args="1,2", kwargs="x=3")
    payload = mock_client.post.call_args[1]["json"]
    assert payload["args"] == "1,2"
    assert payload["kwargs"] == "x=3"


async def test_async_apply_task(registered: FastMCP, mock_client: AsyncMock) -> None:
    mock_client.post.return_value = {"task-id": "xyz"}
    await run(registered, "async_apply_task", taskname="my.task", args="1,2,3")
    mock_client.post.assert_called_once_with(
        "/api/task/async-apply/my.task", json={"args": "1,2,3"}
    )


async def test_send_task(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "send_task", taskname="my.task", kwargs="n=5")
    mock_client.post.assert_called_once_with(
        "/api/task/send-task/my.task", json={"kwargs": "n=5"}
    )


async def test_abort_task(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "abort_task", task_id="abc-123")
    mock_client.post.assert_called_once_with("/api/task/abort/abc-123")


async def test_revoke_task_defaults(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "revoke_task", task_id="abc-123")
    mock_client.post.assert_called_once_with(
        "/api/task/revoke/abc-123",
        params={"terminate": False, "signal": "SIGTERM"},
    )


async def test_revoke_task_terminate(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(registered, "revoke_task", task_id="abc-123", terminate=True, signal="SIGKILL")
    params = mock_client.post.call_args[1]["params"]
    assert params["terminate"] is True
    assert params["signal"] == "SIGKILL"


async def test_set_task_timeout_both(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(
        registered, "set_task_timeout", taskname="my.task", workername="celery@w1", soft=30.0, hard=60.0
    )
    params = mock_client.post.call_args[1]["params"]
    assert params["workername"] == "celery@w1"
    assert params["soft"] == "30.0"
    assert params["hard"] == "60.0"


async def test_set_task_timeout_soft_only(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(
        registered, "set_task_timeout", taskname="my.task", workername="celery@w1", soft=30.0
    )
    params = mock_client.post.call_args[1]["params"]
    assert "hard" not in params
    assert params["soft"] == "30.0"


async def test_set_task_timeout_hard_only(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(
        registered, "set_task_timeout", taskname="my.task", workername="celery@w1", hard=120.0
    )
    params = mock_client.post.call_args[1]["params"]
    assert "soft" not in params
    assert params["hard"] == "120.0"


async def test_set_task_rate_limit(registered: FastMCP, mock_client: AsyncMock) -> None:
    await run(
        registered, "set_task_rate_limit", taskname="my.task", workername="celery@w1", ratelimit="100/m"
    )
    mock_client.post.assert_called_once_with(
        "/api/task/rate-limit/my.task",
        params={"workername": "celery@w1", "ratelimit": "100/m"},
    )
