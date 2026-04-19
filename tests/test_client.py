import httpx
import pytest
from pytest_httpx import HTTPXMock

from source.client import FlowerClient
from source.settings import FlowerSettings


def make_client(**kwargs: object) -> FlowerClient:
    s = FlowerSettings(
        base_url=str(kwargs.get("base_url", "http://localhost:5555")),
        username=kwargs.get("username", None),  # type: ignore[arg-type]
        password=kwargs.get("password", None),  # type: ignore[arg-type]
        api_token=kwargs.get("api_token", None),  # type: ignore[arg-type]
    )
    return FlowerClient(s)


async def test_get_returns_json(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={"workers": 2})
    client = make_client()
    result = await client.get("/api/workers")
    assert result == {"workers": 2}
    await client.aclose()


async def test_get_sends_params(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client()
    await client.get("/api/workers", params={"refresh": True})
    req = httpx_mock.get_request()
    assert req is not None
    assert "refresh=true" in str(req.url)
    await client.aclose()


async def test_post_returns_json(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={"message": "ok"})
    client = make_client()
    result = await client.post("/api/worker/shutdown/celery@w1")
    assert result == {"message": "ok"}
    await client.aclose()


async def test_post_sends_params(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client()
    await client.post("/api/worker/pool/grow/celery@w1", params={"n": 3})
    req = httpx_mock.get_request()
    assert req is not None
    assert "n=3" in str(req.url)
    await client.aclose()


async def test_post_sends_form_data(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client()
    await client.post("/api/task/apply/my.task", data={"args": "[1,2]"})
    req = httpx_mock.get_request()
    assert req is not None
    assert b"args" in req.content
    await client.aclose()


async def test_get_raises_on_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=404)
    client = make_client()
    with pytest.raises(httpx.HTTPStatusError):
        await client.get("/api/workers")
    await client.aclose()


async def test_post_raises_on_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(status_code=503)
    client = make_client()
    with pytest.raises(httpx.HTTPStatusError):
        await client.post("/api/worker/shutdown/celery@w1")
    await client.aclose()


async def test_bearer_token_header(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client(api_token="mytoken")
    await client.get("/api/workers")
    req = httpx_mock.get_request()
    assert req is not None
    assert req.headers["Authorization"] == "Bearer mytoken"
    await client.aclose()


async def test_basic_auth(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client(username="admin", password="pass")
    await client.get("/api/workers")
    req = httpx_mock.get_request()
    assert req is not None
    assert "Authorization" in req.headers
    assert req.headers["Authorization"].startswith("Basic ")
    await client.aclose()


async def test_token_takes_priority_over_basic_auth(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={})
    client = make_client(api_token="tok", username="admin", password="pass")
    await client.get("/api/workers")
    req = httpx_mock.get_request()
    assert req is not None
    assert req.headers["Authorization"] == "Bearer tok"
    await client.aclose()
