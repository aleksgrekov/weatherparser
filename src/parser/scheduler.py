from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.service import Scheduler_SessionFactory
from src.logger.logger import get_logger
from src.repositories.weather_repository import WeatherRepository

logger = get_logger(__name__)


async def add_weather_data_to_db(session: AsyncSession):
    try:
        weather_data = await WeatherRepository.add_weather_data(session)

        if weather_data:
            logger.info("Данные о погоде успешно добавлены!")
        else:
            logger.info("Не удалось получить данные о погоде.")
    except Exception as e:
        logger.warning(f"Ошибка при добавлении данных о погоде: {e}")


async def start_scheduler():
    async with Scheduler_SessionFactory() as session:
        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            add_weather_data_to_db,
            IntervalTrigger(seconds=10),
            args=[session],
            id="weather_data_task",
            name="Добавление данных о погоде",
            replace_existing=True,
        )

        scheduler.start()
