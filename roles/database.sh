#!/bin/bash
echo "Installeren Mariadb database server"
apt update
apt install -y mariadb-server mariadb-client

echo "Enable en start MariaDB service"
systemctl enable mariadb.service
systemctl start mariadb.service

./fw-rules/firewall-base.sh db