from dishka import make_async_container

from source.client import FlowerClient
from source.providers import AppProvider
from source.settings import FlowerSettings


async def test_provider_gives_settings() -> None:
    container = make_async_container(AppProvider())
    settings = await container.get(FlowerSettings)
    assert isinstance(settings, FlowerSettings)
    await container.close()


async def test_provider_gives_client() -> None:
    container = make_async_container(AppProvider())
    client = await container.get(FlowerClient)
    assert isinstance(client, FlowerClient)
    await container.close()


async def test_provider_same_client_instance() -> None:
    container = make_async_container(AppProvider())
    c1 = await container.get(FlowerClient)
    c2 = await container.get(FlowerClient)
    assert c1 is c2
    await container.close()


async def test_client_closed_on_container_close(monkeypatch: object) -> None:
    closed: list[bool] = []

    original_aclose = FlowerClient.aclose

    async def patched_aclose(self: FlowerClient) -> None:
        closed.append(True)
        await original_aclose(self)

    import source.client as client_module

    monkeypatch.setattr(client_module.FlowerClient, "aclose", patched_aclose)  # type: ignore[attr-defined]

    container = make_async_container(AppProvider())
    await container.get(FlowerClient)
    await container.close()
    assert closed == [True]
