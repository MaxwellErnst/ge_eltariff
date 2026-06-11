from __future__ import annotations

import aiohttp
import async_timeout
import logging
from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    sensors = [
        GETariffSensor("current_price"),
        GETariffSensor("next_price"),
        GETariffSensor("current_level"),
        GETariffSensor("current_level_text"),
    ]

    async_add_entities(sensors, True)


class GETariffSensor(SensorEntity):
    """Sensor för Göteborg Energi eltariff."""

    def __init__(self, sensor_type: str) -> None:
        self._type = sensor_type
        self._attr_name = f"GE {sensor_type.replace('_', ' ').title()}"
        self._attr_unique_id = f"ge_eltariff_{sensor_type}"
        self._state = None

    @property
    def state(self):
        return self._state

    async def async_update(self) -> None:
        """Hämta data från Göteborg Energi API."""

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    resp = await session.get(API_URL)

                    if resp.status != 200:
                        _LOGGER.error("GE API returned status %s", resp.status)
                        self._state = None
                        return

                    data = await resp.json()

        except Exception as e:
