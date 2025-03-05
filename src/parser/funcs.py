import json
from typing import Any, Dict, Union

import aiohttp
from geopy.geocoders import Nominatim

from src.models.city_model import City
from src.parser.config import parser_settings

geolocator = Nominatim(user_agent="weather_parser")


async def get_weather(city: "City") -> Union[Dict[str, Any], None]:
    location = geolocator.geocode(city.title)

    if not location:
        return None

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        params = {
            "lat": location.latitude,
            "lon": location.longitude,
            "appid": parser_settings.api_key,
            "units": "metric",
        }

        async with client.get(url=parser_settings.base_url, params=params) as response:
            if response.status == 200:
                result = await response.read()
                data_dict = json.loads(result)

                weather_dict = {
                    "city_id": city.id,
                    "weather": {
                        "temperature": data_dict.get("main").get("temp"),
                        "wind_speed": data_dict.get("wind").get("speed"),
                        "description": data_dict.get("weather")[0].get("description"),
                    }
                }
                return weather_dict

            else:
                return None
