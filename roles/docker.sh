#!/bin/bash
echo "Docker host wordt geïnstalleerd"
echo "Verwijderen oude docker versies"
apt remove -y docker docker-engine docker.io containerd runc

echo "Installeren van pre-requisites"
apt install -y ca-certificates curl gnupg lsb-release curl wget gpg apt-transport-https 

if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
  echo "Aanmaken keyring directory"
  mkdir -p /etc/apt/keyrings

  echo "Toevoegen Docker gpg key aan keyring"
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

  echo "Toevoegen docker repository aan apt soureces en updaten repository"
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt update
fi
echo "Installeren van docker engine"
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Gebruiker toevoegen aan groep"
usermod -aG docker pascal

echo "Starting containers"
# Starten containers. Onder andere Home assistant

containerDir="./roles/files/docker"

for file in ${containerDir}/*; do
  fileName=${file##*/}
  dockerContainer=$(echo $fileName | cut -d'.' -f 1)
  isRunning=$(docker ps -q -f name=${dockerContainer})

  if [[ -z $isRunning ]]; then
    echo "Starten container $file"
    sudo -u pascal $file
  fi
done

echo "Bijwerken firewall regels"
./roles/firewall.sh $1