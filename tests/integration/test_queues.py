import pytest

from source.client import FlowerClient

pytestmark = [pytest.mark.integration, pytest.mark.asyncio(loop_scope="session")]


async def test_healthcheck(client: FlowerClient) -> None:
    result = await client.get("/healthcheck")
    assert result == "OK"


async def test_get_queue_lengths(client: FlowerClient) -> None:
    result = await client.get("/api/queues/length")
    assert isinstance(result, dict)
    # Flower 2.0 returns {"active_queues": [{"name": "celery", "messages": 0}]}
    queues = result.get("active_queues", [])
    assert isinstance(queues, list)
    names = [q["name"] for q in queues]
    assert "celery" in names


async def test_queue_lengths_are_non_negative(client: FlowerClient) -> None:
    result = await client.get("/api/queues/length")
    queues = result.get("active_queues", [])
    for q in queues:
        assert isinstance(q["messages"], int)
        assert q["messages"] >= 0
