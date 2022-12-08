#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Installeren Mariadb database server"
apt update
apt install -y mariadb-server mariadb-client

mysql_secure_installation
echo "Toevoegen 2e admin account."

echo "Enable en start MariaDB service"
systemctl enable mariadb.service
systemctl start mariadb.service

./roles/firewall.sh $1