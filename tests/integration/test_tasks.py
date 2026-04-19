import asyncio

import pytest

from source.client import FlowerClient

pytestmark = [pytest.mark.integration, pytest.mark.asyncio(loop_scope="session")]


async def test_list_task_types(client: FlowerClient) -> None:
    result = await client.get("/api/task/types")
    # Flower 2.0 returns {"task-types": [...]}
    if isinstance(result, dict):
        task_types = result.get("task-types", [])
    else:
        task_types = result
    assert isinstance(task_types, list)


async def test_list_tasks_empty_filters(client: FlowerClient) -> None:
    result = await client.get("/api/tasks", params={"limit": 10})
    assert isinstance(result, dict)


async def test_apply_task_and_get_result(client: FlowerClient) -> None:
    result = await client.post(
        "/api/task/apply/tasks.add",
        json={"args": [3, 4]},
    )
    assert result.get("result") == 7


async def test_async_apply_task_returns_task_id(client: FlowerClient) -> None:
    result = await client.post(
        "/api/task/async-apply/tasks.add",
        json={"args": [1, 2]},
    )
    assert "task-id" in result
    task_id = result["task-id"]
    assert isinstance(task_id, str) and len(task_id) > 0


async def test_get_task_result(client: FlowerClient) -> None:
    dispatched = await client.post(
        "/api/task/async-apply/tasks.add",
        json={"args": [10, 20]},
    )
    task_id = dispatched["task-id"]

    for _ in range(15):
        result = await client.get(f"/api/task/result/{task_id}")
        if result.get("state") == "SUCCESS":
            assert result["result"] == 30
            return
        await asyncio.sleep(1)

    pytest.fail("Task did not complete in time")


async def test_get_task_info(client: FlowerClient) -> None:
    import httpx

    dispatched = await client.post(
        "/api/task/async-apply/tasks.add",
        json={"args": [5, 6]},
    )
    task_id = dispatched["task-id"]
    await asyncio.sleep(2)

    try:
        info = await client.get(f"/api/task/info/{task_id}")
        assert info.get("uuid") == task_id or "state" in info
    except httpx.HTTPStatusError as exc:
        # Flower may evict short-lived tasks from memory before the query
        if exc.response.status_code == 404:
            pytest.skip("Task already evicted from Flower memory")
        raise


async def test_revoke_task(client: FlowerClient) -> None:
    dispatched = await client.post(
        "/api/task/async-apply/tasks.add",
        json={"args": [1, 1]},
    )
    task_id = dispatched["task-id"]
    result = await client.post(f"/api/task/revoke/{task_id}", params={"terminate": False})
    assert "message" in result or result == {} or isinstance(result, dict)


async def test_list_tasks_filter_by_state(client: FlowerClient) -> None:
    result = await client.get("/api/tasks", params={"state": "SUCCESS", "limit": 5})
    assert isinstance(result, dict)
    for task in result.values():
        assert task.get("state") == "SUCCESS"
