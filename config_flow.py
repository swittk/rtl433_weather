import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

DOMAIN = "rtl433_weather"

class Rtl433WeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # If device_id is empty, we store it as None or an empty string
            device_id = user_input.get("device_id", "").strip()
            if not device_id:
                device_id = None  # This means all data will be processed without filtering
            
            user_input["device_id"] = device_id  # Update the input with the adjusted device_id
            return self.async_create_entry(title=user_input["device_name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("mqtt_topic", default="rtl_433/+/events"): cv.string,
                vol.Required("device_name", default="Weather Station"): cv.string,
                vol.Optional("device_model", default="Fineoffset-WHx080"): cv.string,
                vol.Optional("device_id"): cv.string  # Optional device ID filter
            }),
            # Add a descriptive help text below the form
            description_placeholders={
                "mqtt_topic": "Please enter the events stream MQTT topic (e.g., 'rtl_433/raspberrypi/events')."
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return Rtl433WeatherOptionsFlow(config_entry)

class Rtl433WeatherOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("mqtt_topic", default=self.config_entry.data.get("mqtt_topic")): cv.string,
                vol.Optional("device_name", default=self.config_entry.data.get("device_name")): cv.string,
                vol.Optional("device_model", default=self.config_entry.data.get("device_model")): cv.string,
                vol.Optional("device_id", default=self.config_entry.data.get("device_id")): cv.string  # Optional device ID filter
            })
        )
