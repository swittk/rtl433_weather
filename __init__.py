import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import discovery
from .rtl433_weather import async_setup_mqtt

DOMAIN = "rtl433_weather"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the RTL_433 Weather integration."""
    _LOGGER.debug("Setting up RTL_433 Weather integration.")
    return True

async def async_setup_entry(hass, config_entry):
    """Set up RTL_433 Weather integration from a config entry."""
    _LOGGER.debug("Setting up entry for RTL_433 Weather integration.")
    
    # If the sensor platform is used, this forwards the config to sensor.py
    # await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    
    # This function sets up the MQTT connection and subscribes to the necessary topics
    await async_setup_mqtt(hass, config_entry)
    
    return True

async def async_unload_entry(hass, config_entry):
    """Unload RTL_433 Weather integration."""
    _LOGGER.debug("Unloading entry for RTL_433 Weather integration.")
    
    # Unload the sensor platform when the entry is removed
    # await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    
    return True
