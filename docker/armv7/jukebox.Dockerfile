FROM arm32v7/debian:buster-slim

# Prepare Raspberry Pi like environment

# These are only dependencies that are required to get as close to the
# Raspberry Pi environment as possible.
RUN apt-get update && apt-get install -y \
    libasound2-dev \
    pulseaudio \
    pulseaudio-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ARG UID
ARG USER
ARG HOME
ENV INSTALLATION_PATH ${HOME}/RPi-Jukebox-RFID

RUN test ${UID} -gt 0 && useradd -m -u ${UID} ${USER} || continue
RUN usermod -aG pulse ${USER}

# Jukebox
# Install all Jukebox dependencies
RUN apt-get update && apt-get install -qq -y \
    --allow-downgrades --allow-remove-essential --allow-change-held-packages \
    at wget gcc \
    mpc mpg123 git ffmpeg spi-tools netcat alsa-tools \
    python3 python3-venv python3-dev python3-mutagen \
    python3-zmq libzmq5
#samba samba-common-bin
#raspberrypi-kernel-headers
#resolvconf

ENV VIRTUAL_ENV=${INSTALLATION_PATH}/.venv
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# uv (package manager), used below to install Python dependencies as $USER
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN UV_INSTALL_DIR=/usr/local/bin sh /uv-installer.sh && rm /uv-installer.sh

USER ${USER}
WORKDIR ${HOME}
COPY --chown=${USER}:${USER} . ${INSTALLATION_PATH}/

# Install runtime Python dependencies via uv (see pyproject.toml)
RUN cd ${INSTALLATION_PATH} && uv sync --no-dev --no-install-package pyzmq  # python3-zmq apt package instead, uses system libzmq

EXPOSE 5555 5556 5558

WORKDIR ${INSTALLATION_PATH}/src/jukebox

# Run Jukebox
# CMD bash
CMD python ${INSTALLATION_PATH}/src/jukebox/run_jukebox.py
