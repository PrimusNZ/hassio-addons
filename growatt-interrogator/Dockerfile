ARG BUILD_FROM
FROM $BUILD_FROM

# Install packages
RUN apt-get update
RUN apt-get install -y jq tzdata python3 python3-dev python3-pip \
        python3-six python3-pyasn1
RUN pip3 install --upgrade pip
RUN apt-get remove -y --purge python3-pip python3-dev
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

# Copy data
COPY run.sh /
COPY *.py /

RUN chmod a+x /run.sh

ENTRYPOINT [ "/run.sh" ]
