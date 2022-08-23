#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

CLIENT_SECRETS=$(jq --raw-output '.client_secrets' $CONFIG_PATH)

if [ ! -f "$CONFIG_PATH" ]; then
    echo "[Error] You need configure the Growatt Interrogator!"
    exit 1
fi

exec python3 /pv_inverter.py < /dev/null
