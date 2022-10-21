ARG BUILD_FROM
FROM $BUILD_FROM

# Install Server Dependencies for Mycroft
RUN set -x \
	&& apt-get update \
    && apt-get -y upgrade \
	&& apt-get -y install wget procps git python3 python3-pip locales sudo \
    libespeak-ng1 alsa-utils nano \
	&& pip3 install future msm \
	# Checkout Mycroft
	&& git clone https://github.com/MycroftAI/mycroft-core.git /opt/mycroft \
	&& cd /opt/mycroft \
	&& mkdir /opt/mycroft/skills \
	# git fetch && git checkout dev && \ this branch is now merged to master
	&& CI=true /opt/mycroft/./dev_setup.sh --allow-root -sm \
    && mkdir /etc/mycroft \
	&& mkdir /opt/mycroft/scripts/logs \
	&& touch /opt/mycroft/scripts/logs/mycroft-bus.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-voice.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-skills.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-audio.log \
	&& apt-get -y autoremove \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN /opt/mycroft/./bin/mycroft-pip install mycroft-mimic3-tts[all] \
    && /opt/mycroft/./bin/mycroft-pip install mycroft-plugin-tts-mimic3[all] \
    && /opt/mycroft/./bin/mycroft-config set tts.module mimic3_tts_plug

# Set the locale
RUN /bin/sed -i "s/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/" /etc/locale.gen
RUN locale-gen en_US.UTF-8
ENV USER root
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /opt/mycroft
COPY startup.sh /opt/mycroft
COPY mycroft.conf /etc/mycroft
ENV PYTHONPATH $PYTHONPATH:/mycroft/ai

RUN echo "PATH=$PATH:/opt/mycroft/bin" >> $HOME/.bashrc \
        && echo "source /opt/mycroft/.venv/bin/activate" >> $HOME/.bashrc

RUN chmod +x /opt/mycroft/start-mycroft.sh \
	&& chmod +x /opt/mycroft/startup.sh

EXPOSE 8181

ENTRYPOINT "/opt/mycroft/startup.sh"

LABEL org.opencontainers.image.source https://github.com/PrimusNZ/hassio-addons