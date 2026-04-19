from typing import Any

import httpx
from loguru import logger

from source.settings import FlowerSettings


class FlowerClient:
    def __init__(self, settings: FlowerSettings) -> None:
        auth: httpx.BasicAuth | None = None
        headers: dict[str, str] = {}

        if settings.api_token:
            headers["Authorization"] = f"Bearer {settings.api_token}"
        elif settings.username and settings.password:
            auth = httpx.BasicAuth(settings.username, settings.password)

        self._client = httpx.AsyncClient(
            base_url=settings.base_url,
            auth=auth,
            headers=headers,
            timeout=30.0,
        )

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        logger.debug("GET {} params={}", path, params)
        resp = await self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        logger.debug("POST {} params={} data={}", path, params, data)
        resp = await self._client.post(path, params=params, data=data)
        resp.raise_for_status()
        return resp.json()

    async def aclose(self) -> None:
        await self._client.aclose()
