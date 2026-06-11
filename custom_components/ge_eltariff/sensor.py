from __future__ import annotations

import aiohttp
import async_timeout
from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API_URL, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities = [
        GETariffSensor("current_price"),
        GETariffSensor("next_price"),
        GETariffSensor("current_level"),
        GETariffSensor("current_level_text"),
    ]
    async_add_entities(entities, True)


class GETariffSensor(SensorEntity):
    def __init__(self, sensor_type: str) -> None:
        self._type = sensor_type
        self._attr_name = f"GE {sensor_type.replace('_', ' ').title()}"
        self._attr_unique_id = f"ge_eltariff_{sensor_type}"
        self._state = None

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._state

    async def async_update(self) -> None:
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
