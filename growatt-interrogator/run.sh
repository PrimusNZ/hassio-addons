#!/usr/bin/with-contenv bashio
set -e

MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

PVOEnabled=$(bashio::config pvoutput_enabled)
PVOSystemID=$(bashio::config pvoutput_systemid)
PVOAPIKey=$(bashio::config pvoutput_apikey)

OWMKey=$(bashio::config owm_key)
OWMLat=$(bashio::config owm_lat)
OWMLong=$(bashio::config owm_long)

InverterPort=$(bashio::config inverter_port "/dev/ttyUSB0")

cat > /tmp/pvinverter.cfg <<EOF
# Register at pvoutput.org to get your SYSTEMID and APIKEY
PVOEnabled=$PVOEnabled
SystemID=$PVOSystemID
APIKey=$PVOAPIKey

# Inverter
Inverter=$InverterPort

# Register at openweather.org to get your APIKEY
# If OWMKEY and Longitude and Latitude is not supplied
# no weather will be read, and tried uploaded to
# pvoutput.org - together with your energy data.
OWMKEY=$OWMKey
Latitude=$OWMLat
Longitude=$OWMLong

# MQTT For Inverter Interrorgator
MQTTBroker=$MQTT_HOST
MQTTPort=1883
MQTTUser=$MQTT_USER
MQTTPass=$MQTT_PASSWORD
EOF

cat /tmp/pvinverter.cfg

exec python3 /pv_inverter.py < /dev/null
