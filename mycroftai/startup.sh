#!/bin/bash
source /opt/mycroft/.venv/bin/activate

if [ ! -d /data/conf ]; then
    mkdir -p /data/conf
    cp /etc/mycroft/mycroft.conf /data/conf/
fi

/opt/mycroft/./start-mycroft.sh all

tail -f /var/log/mycroft/*.log
