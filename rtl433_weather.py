import json
import logging
from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)

DOMAIN = "rtl433_weather"

async def async_setup_mqtt(hass, config_entry):
    """Set up RTL_433 from a config entry."""
    
    # Get user configuration
    mqtt_topic = config_entry.data.get("mqtt_topic")
    device_name = config_entry.data.get("device_name")
    configured_device_model = config_entry.data.get("device_model")
    configured_device_id = config_entry.data.get("device_id")  # Optional filter for device_id
    
    async def message_received(msg):
        """Handle incoming MQTT messages from RTL_433."""
        data = json.loads(msg.payload)
        
        # Extract relevant fields from the MQTT message
        incoming_device_id = str(data.get("id"))
        incoming_device_model = data.get("model")
        
        # Filter by device model and device ID
        if incoming_device_model != configured_device_model:
            _LOGGER.debug(f"Ignoring message from model {incoming_device_model}, expected {configured_device_model}.")
            return
        
        if configured_device_id and incoming_device_id != configured_device_id:
            _LOGGER.debug(f"Ignoring message from device {incoming_device_id}, expected {configured_device_id}.")
            return

        # Process and publish discovery messages if the device matches the filters
        temperature = data.get("temperature_C")
        humidity = data.get("humidity")
        wind_speed = data.get("wind_avg_km_h")
        wind_direction = data.get("wind_dir_deg")
        wind_max_speed = data.get("wind_max_km_h")
        battery_status = data.get("battery_ok")
        rainfall = data.get("rain_mm")

        if temperature is not None:
            await publish_discovery_message(hass, incoming_device_id, "temperature", "temperature_C", mqtt_topic, "°C", device_name, configured_device_model, configured_device_id)
        if humidity is not None:
            await publish_discovery_message(hass, incoming_device_id, "humidity", "humidity", mqtt_topic, "%", device_name, configured_device_model, configured_device_id)
        if wind_speed is not None:
            await publish_discovery_message(hass, incoming_device_id, "wind_speed", "wind_avg_km_h", mqtt_topic, "km/h", device_name, configured_device_model, configured_device_id)
        if wind_direction is not None:
            await publish_discovery_message(hass, incoming_device_id, "wind_direction", "wind_dir_deg", mqtt_topic, "°", device_name, configured_device_model, configured_device_id)
        if wind_max_speed is not None:
            await publish_discovery_message(hass, incoming_device_id, "wind_max_speed", "wind_max_km_h", mqtt_topic, "km/h", device_name, configured_device_model, configured_device_id)
        if battery_status is not None:
            await publish_discovery_message(hass, incoming_device_id, "battery_status", "battery_ok", mqtt_topic, None, device_name, configured_device_model, configured_device_id)
        if rainfall is not None:
            await publish_discovery_message(hass, incoming_device_id, "rainfall", "rain_mm", mqtt_topic, "mm", device_name, configured_device_model, configured_device_id)

    # Subscribe to the configured MQTT topic
    await mqtt.async_subscribe(hass, mqtt_topic, message_received)

    return True

async def publish_discovery_message(hass, device_id, sensor_type, json_field, mqtt_topic, unit, device_name, device_model, configured_device_id):
    """Publish Home Assistant MQTT discovery message."""
    
    discovery_topic = f"homeassistant/sensor/{device_id}/{sensor_type}/config"
    
    # Update value_template to include ID matching check
    value_template = (
        f"{{% if value_json.id == {configured_device_id} %}}"
        f"{{{{ value_json.{json_field} }}}}"
        f"{{% else %}}"
        f"{{{{ None }}}}"
        f"{{% endif %}}"
    )
    device_class = None
    if sensor_type == "temperature":
        device_class = "temperature"
    elif sensor_type == "humidity":
        device_class = "humidity"
    elif sensor_type == "wind_speed":
        device_class = "wind_speed"
    elif sensor_type == "wind_max_speed":
        device_class = "wind_speed"

    discovery_payload = {
        "name": f"{device_name} {sensor_type.capitalize()}",
        "state_topic": mqtt_topic,  # Use the configured mqtt_topic here
        "value_template": value_template,  # Conditionally extract the field if ID matches
        "unit_of_measurement": unit,
        "device_class": device_class,
        "unique_id": f"{device_id}_{sensor_type}",
        "device": {
            "identifiers": [f"{device_model}_{device_id}"],
            "name": device_name,
            "model": device_model,
            "manufacturer": "RTL_433"
        }
    }

    await mqtt.async_publish(hass, discovery_topic, json.dumps(discovery_payload))
    _LOGGER.info(f"Published discovery message for {sensor_type}")

# async def publish_discovery_message(hass, device_id, sensor_type, json_field, mqtt_topic, unit, model):
#     """Publish Home Assistant MQTT discovery message."""
#     discovery_topic = f"homeassistant/sensor/{device_id}/{sensor_type}/config"

#     # Map supported device_class values
#     device_class = None
#     if sensor_type == "temperature":
#         device_class = "temperature"
#     elif sensor_type == "humidity":
#         device_class = "humidity"
#     elif sensor_type == "wind_speed":
#         device_class = "wind_speed"

#     # Device-specific value_template to filter by device_id
#     value_template = f"{{{{ value_json.{json_field} if value_json.id == {device_id} else none }}}}"

#     discovery_payload = {
#         "name": f"{model} {sensor_type.capitalize()}",
#         "state_topic": mqtt_topic,
#         "value_template": value_template,  # Filter based on device_id
#         "unit_of_measurement": unit,
#         "device_class": device_class,  # Only use valid device_class values
#         "unique_id": f"{device_id}_{sensor_type}",
#         "device": {
#             "identifiers": [f"{model}_{device_id}"],
#             "name": model,
#             "model": model,
#             "manufacturer": "RTL_433"
#         }
#     }

#     # Publish the discovery payload to the appropriate topic
#     await mqtt.async_publish(hass, discovery_topic, json.dumps(discovery_payload))
#     _LOGGER.info(f"Published discovery message for {sensor_type}")
