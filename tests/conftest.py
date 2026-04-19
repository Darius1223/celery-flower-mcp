from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from source.client import FlowerClient


@pytest.fixture
def mock_client() -> AsyncMock:
    client = AsyncMock(spec=FlowerClient)
    client.get = AsyncMock(return_value={})
    client.post = AsyncMock(return_value={"message": "ok"})
    return client


@pytest.fixture
def mcp() -> FastMCP:
    return FastMCP("test")


@pytest.fixture
def mock_settings() -> MagicMock:
    s = MagicMock()
    s.base_url = "http://localhost:5555"
    s.username = None
    s.password = None
    s.api_token = None
    return s
