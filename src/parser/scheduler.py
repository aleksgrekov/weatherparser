from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.database.service import Scheduler_SessionFactory
from src.logger.logger import get_logger
from src.repositories.weather_repository import WeatherRepository

logger = get_logger(__name__)


async def add_weather_data_to_db():
    """
    Функция для получения данных о погоде и добавления их в базу данных.
    Логирует успех или ошибку в процессе получения и добавления данных.

    Параметры:
    - session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    """
    async with Scheduler_SessionFactory() as session:
        weather_data = await WeatherRepository.add_weather_data(session)

        if weather_data:
            logger.info("Данные о погоде успешно добавлены в базу данных!")
        else:
            logger.info("Не удалось получить данные о погоде.")


async def start_scheduler():
    """
    Запуск шедулера для периодического получения данных о погоде.
    Шедулер будет выполнять задачу по получению данных о погоде с заданным интервалом.
    """

    scheduler = AsyncIOScheduler()

    # Добавление задачи в шедулер, которая будет выполняться с заданным интервалом.
    scheduler.add_job(
        add_weather_data_to_db,  # Функция, которая будет выполняться
        IntervalTrigger(minutes=2),  # Интервал запуска задачи
        id="weather_data_task",  # Уникальный идентификатор задачи
        name="Задача по добавлению данных о погоде",  # Имя задачи
        replace_existing=True,  # Если задача с таким ID уже существует, заменим её
        max_instances=2,
    )

    # Запуск шедулера
    scheduler.start()
