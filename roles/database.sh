#!/bin/bash
echo "Installeren Mariadb database server"
apt update
apt install -y mariadb-server mariadb-client curl wget gpg apt-transport-https

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

mysql_secure_installation
echo "Toevoegen 2e admin account."

echo "Configureren voor inkomend verkeer van LAN"
sed -i 's/bind-address/#bind-address/' /etc/mysql/mariadb.conf.d/50-server.cnf

echo "Enable en start MariaDB service"
systemctl enable mariadb.service
systemctl restart mariadb.service

./roles/firewall.sh $1