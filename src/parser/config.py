from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseSettings):
    """
    Конфигурация для парсера, загружающая настройки из файла .env.
    Содержит ключ API и базовый URL для запросов к внешнему API погоды.
    """

    API_KEY: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",  # Игнорировать дополнительные поля, если они есть в конфиге
    )

    @property
    def api_key(self) -> str:
        """
        Возвращает ключ API для работы с внешним сервисом.

        Возвращает:
            str: Ключ API.
        """
        return self.API_KEY

    @property
    def base_url(self) -> str:
        """
        Возвращает базовый URL для запросов к внешнему API.

        Возвращает:
            str: Базовый URL.
        """
        return self.BASE_URL


parser_settings: ParserSettings = ParserSettings()  # type: ignore
