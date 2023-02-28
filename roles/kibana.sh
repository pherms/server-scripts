#!/bin/bash
echo "Elasticsearch en Kibana worden geïnstalleerd."
echo "Installeren packages."
apt install -y default-jre nginx gpg curl apt-transport-https wget

echo "Installeren van elasticsearch, kibana, metricbeat, filebeat, logstash en elastic-agent"
apt install -y elasticsearch kibana logstash 

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