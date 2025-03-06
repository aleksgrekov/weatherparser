from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.service import Scheduler_SessionFactory
from src.logger.logger import get_logger
from src.repositories.weather_repository import WeatherRepository

logger = get_logger(__name__)


async def add_weather_data_to_db(session: AsyncSession):
    """
    Функция для получения данных о погоде и добавления их в базу данных.
    Логирует успех или ошибку в процессе получения и добавления данных.

    Параметры:
    - session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    """
    try:
        weather_data = await WeatherRepository.add_weather_data(session)

        if weather_data:
            logger.info("Данные о погоде успешно добавлены в базу данных!")
        else:
            logger.info("Не удалось получить данные о погоде.")
    except Exception as e:
        logger.warning(f"Ошибка при добавлении данных о погоде: {e}")


async def start_scheduler():
    """
    Запуск шедулера для периодического получения данных о погоде.
    Шедулер будет выполнять задачу по получению данных о погоде каждые 10 секунд.
    """
    async with Scheduler_SessionFactory() as session:
        scheduler = AsyncIOScheduler()

        # Добавление задачи в шедулер, которая будет выполняться с заданным интервалом.
        scheduler.add_job(
            add_weather_data_to_db,  # Функция, которая будет выполняться
            IntervalTrigger(minutes=1),  # Интервал запуска задачи
            args=[session],  # Передаем сессию как аргумент
            id="weather_data_task",  # Уникальный идентификатор задачи
            name="Задача по добавлению данных о погоде",  # Имя задачи
            replace_existing=True,  # Если задача с таким ID уже существует, заменим её
        )

        # Запуск шедулера
        scheduler.start()
