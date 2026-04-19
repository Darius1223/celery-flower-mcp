from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FlowerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FLOWER_",
        env_file=".env",
        extra="ignore",
    )

    url: str = Field(default="http://localhost:5555")
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    api_token: str | None = Field(default=None)

    @property
    def base_url(self) -> str:
        return self.url
