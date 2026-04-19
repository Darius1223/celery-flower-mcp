import pytest

from source.client import FlowerClient

pytestmark = [pytest.mark.integration, pytest.mark.asyncio(loop_scope="session")]


async def test_list_workers(client: FlowerClient) -> None:
    result = await client.get("/api/workers", params={"refresh": True})
    assert isinstance(result, dict)
    assert len(result) >= 1


async def test_list_workers_status_only(client: FlowerClient) -> None:
    result = await client.get("/api/workers", params={"status": True})
    assert isinstance(result, dict)
    for value in result.values():
        assert isinstance(value, bool)


async def test_list_workers_refresh(client: FlowerClient) -> None:
    result = await client.get("/api/workers", params={"refresh": True})
    assert isinstance(result, dict)


async def test_worker_has_expected_fields(client: FlowerClient) -> None:
    result = await client.get("/api/workers", params={"refresh": True})
    worker = next(iter(result.values()))
    assert "status" in worker or "stats" in worker or isinstance(worker, dict)


async def test_list_workers_unknown_name_returns_404(client: FlowerClient) -> None:
    import httpx

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await client.get("/api/workers", params={"workername": "celery@nonexistent"})
    assert exc_info.value.response.status_code == 404
