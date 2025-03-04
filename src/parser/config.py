from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseSettings):
    API_KEY: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
    )

    @property
    def api_key(self):
        return self.API_KEY

    @property
    def base_url(self):
        return self.BASE_URL


parser_settings: ParserSettings = ParserSettings()  # type: ignore
