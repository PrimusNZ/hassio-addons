#!/bin/bash
source /opt/mycroft/.venv/bin/activate

if [ ! -d /data/config ]; then
    cp -av /var/cache/mycroft/* /data/
fi

/opt/mycroft/./start-mycroft.sh all

tail -f /var/log/mycroft/*.log
