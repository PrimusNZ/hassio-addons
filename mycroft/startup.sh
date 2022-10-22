#!/bin/bash
source /opt/mycroft/.venv/bin/activate

if [ ! -d /data/conf ]; then
    mkdir -p /data/conf
    cp /etc/mycroft/mycroft.conf /data/conf/
fi

if [ ! -d /data/local ]; then
    mkdir -p /data/local
    /opt/mycroft/.venv/bin/mimic3 --preload-voice en_UK/apope_low
fi

/opt/mycroft/./start-mycroft.sh all

tail -f /var/log/mycroft/*.log
