# RTL 433 Autodiscovery integration for RTL_433 weather stations
I made this to work with my Fineoffset weather station, which sends data to the RTL-SDR receiver on my server which uses RTL_433 to send data to the standard MQTT of my house.
This integration discovers the MQTT weather events from the device with the specified ID, and allows the broadcasted parameters to be autodiscovered by HomeAssistant.
Seemed no other integration-based solution existed yet (I don't want to maintain a bunch of config.yml for custom sensors that I'll forget where they exist or how to set-up again), so I made this to quickly get something functional.

# Usage
Download, then add the integration to `config/custom_components/rtl433_weather`
When you add the integration in the UI, you'll need to enter
1. the MQTT topic for the events (e.g. for default RTL_433 configuration, it'll be `rtl_433/computer_name/events`)
2. preferred name for your weather station
3. preferred device model to display
4. device_id of the weather station (you can see this in the `/events` stream raw data, which should have the "id" field)

After doing so, the integration will subscribe to the MQTT events, and publish a HomeAssistant-compatible autodiscoverable events stream. Your device should show up on the dashboard with little hassle :)

Special Tips : For FineOffset weather stations, it seems that the rainfall sensor only shows total accumulated lifetime rainfall. For a display that's more useful, you can add hourly/24h rainfall metering by going to Home assistant's Helpers section (Settings/Devices & services/Helpers) and create a derivative sensor over the time period you want!

<img width="418" alt="Screen Shot 2567-10-01 at 21 33 45" src="https://github.com/user-attachments/assets/aabbfd79-db1c-448b-b826-50db828d9653">
<img width="411" alt="Screen Shot 2567-10-01 at 21 34 14" src="https://github.com/user-attachments/assets/af4b83cc-29ac-460a-b778-38d50e772d64">

# License
MIT
