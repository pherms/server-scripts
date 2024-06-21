#!/bin/bash
echo "Opvragen hostname"
hostname=$(cat /etc/hostname)

echo "Gevonden hostname: $hostname"

echo "Mailserver wordt geïnstalleerd"
echo "Installeren packages"

apt install -y postfix openssl mailutils curl wget gpg apt-transport-https 

echo "Writing postfix configuration"
yes | cp ./roles/files/postfix/* /etc/postfix/

echo "Update /etc/postfix/sasl_passwd"

echo "Postfix is geconfigureerd"
echo "Start en enable postfix service"

systemctl enable postfix
systemctl start postfix

./roles/firewall.sh $1