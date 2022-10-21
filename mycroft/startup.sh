#!/bin/bash
source /opt/mycroft/.venv/bin/activate

if [ ! -d /data ]; then
    mkdir /data
fi

if [ ! -f /data/mycroft.conf ]; then
    cp /etc/mycroft/mycroft.conf /data/
fi

/opt/mycroft/./start-mycroft.sh all

tail -f /var/log/mycroft/*.log
