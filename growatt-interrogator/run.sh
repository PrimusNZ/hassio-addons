#!/usr/bin/with-contenv bashio
set -e

MQTT_HOST=$(bashio::services mqtt "host")
MQTT_USER=$(bashio::services mqtt "username")
MQTT_PASSWORD=$(bashio::services mqtt "password")

PVO_Enabled=$(bashio::config pvoutput_enabled)
PVO_SystemID=$(bashio::config pvoutput_systemid)
PVO_APIKey=$(bashio::config pvoutput_apikey)

InverterPort=$(bashio::config inverter_port "/dev/ttyUSB0")

Verbose=$(bashio::config verbose)

cat > /tmp/pvinverter.cfg <<EOF
# Register at pvoutput.org to get your SYSTEMID and APIKEY
PVOEnabled=$PVO_Enabled
SystemID=$PVO_SystemID
APIKey=$PVO_APIKey

# Inverter
Inverter=$InverterPort

# Logging
Verbose=$Verbose

# MQTT For Inverter Interrorgator
MQTTBroker=$MQTT_HOST
MQTTPort=1883
MQTTUser=$MQTT_USER
MQTTPass=$MQTT_PASSWORD
EOF

exec python3 /interrogator.py < /dev/null
