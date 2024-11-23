from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback

from . import DOMAIN  # DSM integration's domain constant


@config_entries.HANDLERS.register(DOMAIN)
class DSMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DSM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate input here
            if "@" not in user_input["email"] or "." not in user_input["email"]:
                errors["email"] = "invalid_email"
            elif len(user_input["password"]) < 6:
                errors["password"] = "password_too_short"
            else:
                # Save the config entry
                return self.async_create_entry(
                    title=user_input["api_endpoint"],
                    data={
                        "api_endpoint": user_input["api_endpoint"],
                        "email": user_input["email"],
                        "password": user_input["password"],
                    },
                )

        # Schema for the input form
        schema = vol.Schema(
            {
                vol.Required("api_endpoint"): str,
                vol.Required("email"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return DSMOptionsFlowHandler(config_entry)


class DSMOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for DSM."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for DSM."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Options step."""
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input
            )
            return self.async_create_entry(title="", data=None)

        schema = vol.Schema(
            {
                vol.Required("email", default=self.config_entry.data.get("email")): str,
                vol.Required(
                    "password", default=self.config_entry.data.get("password")
                ): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)
