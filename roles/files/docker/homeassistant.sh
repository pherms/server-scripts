#!/bin/bash
# Stappen om homeassistant container te downloaden en te starten.
timeZone="Europe/Amsterdam"
configPath="/opt/homeassistant"

echo "Maken van directory $configPath"
if [[ ! -d ${configPath} ]]; then
    mkdir -p ${configPath}
fi

docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=${timeZone} \
  -v ${configPath}:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable