import json
from typing import Any, Dict, Optional

import aiohttp
from geopy.geocoders import Nominatim

from src.logger.logger import get_logger
from src.models.city_model import City
from src.parser.config import parser_settings

geolocator = Nominatim(user_agent="weather_parser")

logger = get_logger(__name__)


async def get_weather(city: City) -> Optional[Dict[str, Any]]:
    """
    Асинхронная функция для получения данных о погоде по названию города.
    Использует API для получения информации о погоде, включая температуру, скорость ветра и описание.

    Параметры:
    - city: Экземпляр модели города, который содержит название города и его ID.

    Возвращает:
    - weather_dict: Словарь с данными о погоде (температура, скорость ветра, описание).
    - None: Если город не найден или произошла ошибка при запросе данных.
    """
    location = geolocator.geocode(city.title)

    if not location:
        return None

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        params = {
            "lat": location.latitude,
            "lon": location.longitude,
            "appid": parser_settings.api_key,
            "units": "metric",  # Температура в градусах Цельсия
        }

        try:
            async with client.get(
                url=parser_settings.base_url, params=params
            ) as response:
                if response.status == 200:
                    result = await response.read()
                    data_dict = json.loads(result)

                    # Проверка на наличие нужных данных в ответе
                    main_data = data_dict.get("main", {})
                    wind_data = data_dict.get("wind", {})
                    weather_data = data_dict.get("weather", [{}])[0]

                    weather_dict = {
                        "city_id": city.id,
                        "temperature": main_data.get("temp"),
                        "wind_speed": wind_data.get("speed"),
                        "description": weather_data.get("description"),
                    }

                    return weather_dict
                else:
                    # В случае ошибки с API
                    return None
        except aiohttp.ClientError as e:
            logger.warning("fОшибка при запросе данных о погоде: {e}")
            return None
