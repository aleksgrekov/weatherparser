from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """
    Класс для управления настройками подключения к базе данных PostgreSQL.

    Настройки загружаются из переменных окружения или файла `.env`.
    """

    MODE: str

    DB_HOST: str  # Хост базы данных
    DB_PORT: int  # Порт базы данных
    DB_USER: str  # Имя пользователя базы данных
    DB_PASSWORD: str  # Пароль пользователя базы данных
    DB_NAME: str  # Название базы данных

    def db_url(self, driver: Optional[str] = None) -> str:
        """
        Формирует URL для подключения к базе данных PostgreSQL.

        :param driver: Опциональный драйвер подключения (например, 'asyncpg').
        :return: Строка с URL подключения к базе данных.
        """
        return "postgresql{driver}://{user}:{password}@{host}:{port}/{name}".format(
            driver=f"+{driver}" if driver else "",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent
        / ".env",  # Путь к файлу .env
        extra="ignore",  # Игнорировать лишние переменные окружения
    )


# Создание глобального экземпляра настроек базы данных
db_settings: DBSettings = DBSettings()  # type: ignore
