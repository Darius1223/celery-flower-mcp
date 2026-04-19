import os
import time
import urllib.error
import urllib.request
from collections.abc import AsyncIterator

import pytest

from source.client import FlowerClient
from source.settings import FlowerSettings

FLOWER_URL = os.getenv("FLOWER_URL", "http://localhost:5555")
READY_TIMEOUT = 90

# All integration tests share the session event loop to avoid cross-loop transport errors
pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.fixture(scope="session", autouse=True)
def wait_for_flower() -> None:
    deadline = time.time() + READY_TIMEOUT
    last_error: Exception = TimeoutError("not started")
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{FLOWER_URL}/healthcheck", timeout=3)
            return
        except Exception as exc:
            last_error = exc
            time.sleep(3)
    raise TimeoutError(
        f"Flower at {FLOWER_URL} not ready after {READY_TIMEOUT}s: {last_error}"
    )


@pytest.fixture(scope="session")
async def flower_client(wait_for_flower: None) -> AsyncIterator[FlowerClient]:
    fc = FlowerClient(FlowerSettings(url=FLOWER_URL))
    yield fc
    await fc.aclose()


@pytest.fixture
def client(flower_client: FlowerClient) -> FlowerClient:
    return flower_client
