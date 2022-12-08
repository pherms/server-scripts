#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Installing nginx"
apt update
apt install -y nginx nginx-doc

echo "Start en enable nginx"
systemctl enable nginx
systemctl start nginx

echo "Disable default virtual host"
unlink /etc/nginx/sites-enabled/default

#./roles/firewall.sh $1