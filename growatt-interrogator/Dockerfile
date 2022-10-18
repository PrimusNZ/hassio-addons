ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install packages
RUN apt-get update
RUN apt-get install -y jq tzdata python3 python3-paho-mqtt python3-pymodbus python3-requests python3-configobj python3-apscheduler
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

# Copy data
COPY run.sh /
COPY *.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
