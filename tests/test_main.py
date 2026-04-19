from unittest.mock import AsyncMock, patch

from mcp.server.fastmcp import FastMCP

import source.main as main_module
from source.client import FlowerClient


async def test_lifespan_registers_tools_and_closes_container() -> None:
    mock_client = AsyncMock(spec=FlowerClient)
    mock_container = AsyncMock()
    mock_container.get = AsyncMock(return_value=mock_client)

    test_mcp = FastMCP("test-lifespan")

    with patch.object(main_module, "container", mock_container):
        async with main_module.lifespan(test_mcp):
            tools = [t.name for t in test_mcp._tool_manager.list_tools()]
            assert "list_workers" in tools
            assert "list_tasks" in tools
            assert "get_queue_lengths" in tools

    mock_container.close.assert_called_once()


async def test_lifespan_yields_empty_dict() -> None:
    mock_client = AsyncMock(spec=FlowerClient)
    mock_container = AsyncMock()
    mock_container.get = AsyncMock(return_value=mock_client)

    test_mcp = FastMCP("test-lifespan2")

    with patch.object(main_module, "container", mock_container):
        async with main_module.lifespan(test_mcp) as ctx:
            assert ctx == {}
