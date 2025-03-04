from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.database.service import Scheduler_SessionFactory
from src.repositories.weather_repository import WeatherRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def add_weather_data_to_db(session: AsyncSession):
    try:
        weather_data = await WeatherRepository.add_weather_data(session)

        if weather_data:
            print("Данные о погоде успешно добавлены!")
        else:
            print("Не удалось получить данные о погоде.")
    except Exception as e:
        print(f"Ошибка при добавлении данных о погоде: {e}")


async def start_scheduler():
    async with Scheduler_SessionFactory() as session:
        scheduler = AsyncIOScheduler()

        scheduler.add_job(
            add_weather_data_to_db,
            IntervalTrigger(seconds=15),
            args=[session],
            id="weather_data_task",
            name="Добавление данных о погоде",
            replace_existing=True
        )

        scheduler.start()
