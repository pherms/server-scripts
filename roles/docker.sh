#!/bin/bash
echo "Docker host wordt geïnstalleerd"
echo "Verwijderen oude docker versies"
apt remove -y docker docker-engine docker.io containerd runc

echo "Installeren van pre-requisites"
apt install -y ca-certificates curl gnupg lsb-release curl wget gpg apt-transport-https 

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

echo "Aanmaken keyring directory"
mkdir -p /etc/apt/keyrings

echo "Toevoegen Docker gpg key aan keyring"
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "Toevoegen docker repository aan apt soureces en updaten repository"
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update

echo "Installeren van docker engine"
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Starting containers"
# Starten containers. Onder andere Home assistant
./roles/docker/homeassistant.sh

echo "Bijwerken firewall regels"
./roles/firewall.sh $1