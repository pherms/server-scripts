#!/bin/bash
echo "Elasticsearch en Kibana worden geïnstalleerd."
echo "Installeren packages."
apt install -y default-jre nginx gpg curl apt-transport-https wget

echo "Installeren van elasticsearch, kibana, metricbeat, filebeat, logstash en elastic-agent"
apt install -y elasticsearch kibana logstash 

echo "Opvragen IP adres"
ipAddress=$(ip route | awk '/192.168.2/ { print $9 }')

echo "Updaten elasticsearch config file"
sed -i 's/#network.host/network.host/' /etc/elasticsearch/elasticsearch.yml
sed -i "s/192.168.0.1/$ipAddress/" /etc/elasticsearch/elasticsearch.yml
sed -i 's/#http.port/http.port/' /etc/elasticsearch/elasticsearch.yml

echo "Controleren of de elasticsearch service is gestart"
isElasticRunning=$(systemctl status elasticsearch | grep '(running)')
if [[ "$isElasticRunning" != "running" ]]; then
    echo "Start en enable de elasticsearch service"
    systemctl start elasticsearch
    systemctl enable elasticsearch
else
    echo "De Metricbeat service is al actief"
fi

echo "Controleren of de kibana service is gestart"
isKibanaRunning=$(systemctl status kibana | grep '(running)')
if [[ "$isKibanaRunning" != "running" ]]; then
    echo "Start en enable de kibana service"
    systemctl start kibana
    systemctl enable kibana
else
    echo "De Kibana service is al actief"
fi

echo "Updaten metricbeat config file"
sed -i 's/#host:/host:/' /etc/metricbeat/metricbeat.yml
sed -i 's/#hosts:/hosts:/' /etc/metricbeat/metricbeat.yml

echo "Controleren of de metricbeat service is gestart"
isMetricbeatRunning=$(systemctl status metricbeat | grep '(running)')

if [[ "$isMetricbeatRunning" != "running" ]]; then
    echo "Start en enable de metricbeat service"
    systemctl start metricbeat
    systemctl enable metricbeat
else
    echo "De Metricbeat service is al actief"
fi

echo "Bijwerken firewall regels"
./roles/firewall.sh $1