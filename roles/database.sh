#!/bin/bash
echo "Installeren Mariadb database server"
apt update
apt install -y mariadb-server mariadb-client curl wget gpg apt-transport-https

mysql_secure_installation
echo "Toevoegen 2e admin account."

echo "Configureren voor inkomend verkeer van LAN"
sed -i 's/bind-address/#bind-address/' /etc/mysql/mariadb.conf.d/50-server.cnf

echo "Enable en start MariaDB service"
systemctl enable mariadb.service
systemctl restart mariadb.service

./roles/firewall.sh $1