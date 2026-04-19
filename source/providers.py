from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide

from source.client import FlowerClient
from source.settings import FlowerSettings


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def get_settings(self) -> FlowerSettings:
        return FlowerSettings()

    @provide
    async def get_client(self, settings: FlowerSettings) -> AsyncIterator[FlowerClient]:
        client = FlowerClient(settings)
        yield client
        await client.aclose()
