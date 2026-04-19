import pytest

from source.settings import FlowerSettings


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("FLOWER_URL", "FLOWER_USERNAME", "FLOWER_PASSWORD", "FLOWER_API_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    s = FlowerSettings()
    assert s.base_url == "http://localhost:5555"
    assert s.username is None
    assert s.password is None
    assert s.api_token is None


def test_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FLOWER_URL", "http://flower:5555")
    monkeypatch.setenv("FLOWER_USERNAME", "admin")
    monkeypatch.setenv("FLOWER_PASSWORD", "secret")
    monkeypatch.setenv("FLOWER_API_TOKEN", "tok123")
    s = FlowerSettings()
    assert s.base_url == "http://flower:5555"
    assert s.username == "admin"
    assert s.password == "secret"
    assert s.api_token == "tok123"


def test_partial_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FLOWER_URL", raising=False)
    monkeypatch.setenv("FLOWER_USERNAME", "user")
    monkeypatch.delenv("FLOWER_PASSWORD", raising=False)
    monkeypatch.delenv("FLOWER_API_TOKEN", raising=False)
    s = FlowerSettings()
    assert s.base_url == "http://localhost:5555"
    assert s.username == "user"
    assert s.password is None
