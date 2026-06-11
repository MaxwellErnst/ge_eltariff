import aiohttp
import async_timeout
from datetime import datetime, timezone
from homeassistant.components.sensor import SensorEntity
from .const import API_URL

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities(
        [
            GETariffSensor("current_price"),
            GETariffSensor("next_price"),
            GETariffSensor("current_level"),
            GETariffSensor("current_level_text"),
        ],
        True,
    )

class GETariffSensor(SensorEntity):
    def __init__(self, sensor_type):
        self._type = sensor_type
        self._state = None
        self._attr_name = f"GE {sensor_type.replace('_', ' ').title()}"

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(API_URL) as resp:
                    data = await resp.json()

        tariffs = data["tariffs"][0]["prices"]
        now = datetime.now(timezone.utc)

        current = None
        next_price = None

        for t in tariffs:
            start = datetime.fromisoformat(t["startTime"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(t["endTime"].replace("Z", "+00:00"))

            if start <= now < end:
                current = t

            if start > now and next_price is None:
                next_price = t

        if self._type == "current_price":
            self._state = current["price"] if current else None

        elif self._type == "next_price":
            self._state = next_price["price"] if next_price else None

        elif self._type == "current_level":
            self._state = current["level"] if current else None

        elif self._type == "current_level_text":
            lvl = current["level"] if current else None
            mapping = {"HIGH": "Höglast", "LOW": "Låglast", "NORMAL": "Normal"}
            self._state = mapping.get(lvl, "Okänd")
