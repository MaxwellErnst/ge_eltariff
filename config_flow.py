import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_TARIFF,
    CONF_POWER_SENSOR,
    CONF_INCLUDE_VAT,
    TARIFFS,
)


class GöteborgEnergiConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):

        if user_input is not None:
            return self.async_create_entry(
                title="Göteborg Energi",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_TARIFF): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(TARIFFS.keys())
                    )
                ),
                vol.Optional(CONF_POWER_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor"
                    )
                ),
                vol.Required(
                    CONF_INCLUDE_VAT,
                    default=True,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return GöteborgEnergiOptionsFlow(config_entry)


class GöteborgEnergiOptionsFlow(
    config_entries.OptionsFlow
):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input=None,
    ):

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_TARIFF,
                    default=self.config_entry.options.get(
                        CONF_TARIFF,
                        self.config_entry.data.get(CONF_TARIFF),
                    ),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(TARIFFS.keys())
                    )
                ),
                vol.Optional(
                    CONF_POWER_SENSOR,
                    default=self.config_entry.options.get(
                        CONF_POWER_SENSOR,
                        self.config_entry.data.get(
                            CONF_POWER_SENSOR
                        ),
                    ),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor"
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )
