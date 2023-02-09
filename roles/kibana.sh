#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Elasticsearch en Kibana worden geïnstalleerd."
echo "Installeren packages."
apt install -y default-jre nginx gpg curl apt-transport-https wget

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elasticsearch, kibana, metricbeat, filebeat, logstash en elastic-agent"
apt install -y elasticsearch kibana metricbeat filebeat logstash elastic-agent

echo "Updaten elasticsearch config file"
sed -i 's/#network.host/network.host/' /etc/elasticsearch/elasticsearch.yml
sed -i 's/#http.port/http.port/' /etc/elasticsearch/elasticsearch.yml

echo "Start en enable de elasticsearch service"
systemctl start elasticsearch
systemctl enable elasticsearch

echo "Start en enable de kibana service"
systemctl start kibana
systemctl enable kibana

echo "Updaten metricbeat config file"
sed -i 's/#host:/host:/' /etc/metricbeat/metricbeat.yml
sed -i 's/#hosts:/hosts:/' /etc/metricbeat/metricbeat.yml

echo "Start en enable de metricbeat service"
systemctl start metricbeat
systemctl enable metricbeat

echo "Bijwerken firewall regels"
./roles/firewall.sh $1