from __future__ import annotations

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN


class GETariffConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow för Göteborg Energi eltariff."""
    
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Första (och enda) steget i flödet."""
        
        if user_input is not None:
            # Skapa integrationen direkt – inga inställningar behövs
            return self.async_create_entry(
                title="Göteborg Energi El-tariff",
                data={}
            )

        # Visa ett tomt formulär (krävs av Home Assistant)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
