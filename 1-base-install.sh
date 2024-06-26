#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

# ask dns server and domain name
read -p "Wat is de dns server?: " dnsserver

# ask domain name
read -p "Wat is de domain name?: " domainname

# ask if server-config db al bestaat

# Set hostname
read -p "Wat is de hostnaam van deze server?: " hostname

# ask db password
read -p "Wat is het password voor de database?: " dbpassword

# ask db server
read -p "Wat is de databaseserver?: " dbserver

echo "Setting hostname"
hostnamectl set-hostname $hostname

serverapidir="/opt/server-api/"
clientconfigdir="/var/www/client-config/"

# Setup regular user
read -p "Normale gebruiker toevoegen? (Y/N): " addRegularUser
# if [[ "${addRegularUser,,}" = "y" ]]; then
#   GetPassword
#   if [[ "$password1" = "$password2" ]]; then
#     echo "Passwords do match"
#     password=$password1
#   else
#     GetPassword
#   fi
# fi

# if [ "${addRegularUser,,}" = "y" ]; then
#   #add regular user
#   useradd -m -s /bin/bash -p $(openssl passwd -crypt $password) -G sudo,backup $userName
# fi

# update sources-list
isContrib=$(grep "main contrib non-free" /etc/apt/sources.list)
if [[ -z "$isContrib" ]]; then
  echo "non-free repos not enabled; enabling..."
  sed -i 's/main/main non-free-firmware/' /etc/apt/sources.list
fi

apt update -y
apt install -y git sudo screenfetch intel-microcode initramfs-tools firmware-linux lshw openssh-server prometheus-node-exporter dnsutils systemd-resolved rsync ntp acl python3 python3-pip python3-requests nodejs npm apache2 postgresql-client
# pm2
# npm install -g pm2

# create backup directory
mkdir -p /vol/backup

# create config directory
mkdir -p /etc/server-scripts

if [[ ! -d $serverapidir ]]; then
  mkdir -p ${serverapidir}middlewares/authorization
  mkdir -p ${serverapidir}config
fi

echo "DATABASE_URL=\"postgresql://serverconfig:$dbpassword@$dbserver:5432/serverconfig\"" >> $serverapidir.env
echo "PORT=8081" >> $serverapidir.env

if [[ ! -d $clientconfigdir ]]; then
  mkdir -p $clientconfigdir
fi

cp /scripts/server-scripts/roles/files/apache/config.conf /etc/apache2/sites-available/
chown -R www-data:www-data $clientconfigdir

python3 /scripts/server-scripts/backup/installconfig.py
# copy source naar $serverapidir, dan npm install, dan npx prisma generate

a2ensite config.conf
a2enmod headers

# Kopieren van bestanden
yes | cp /scripts/server-scripts/backup/systemd/* /etc/systemd/system/
yes | cp /scripts/server-scripts/backup/backup-config.json /etc/server-scripts/backup-config.json
yes | cp /scripts/server-scripts/backup/sources /etc/server-scripts/

Configure DNS
resolvectl dns ens18 $dnsserver
resolvectl domain ens18 $domainname

# reload systemctl daemon en enable en start services
systemctl daemon-reload
systemctl restart apache2
systemctl enable ssh.service
systemctl start ssh.service
systemctl enable prometheus-node-exporter.service
systemctl start prometheus-node-exporter.service
systemctl restart systemd-resolved.service
systemctl enable backup.timer
systemctl start backup.timer
systemctl enable autoupdate.timer
systemctl start autoupdate.timer
systemctl enable backup.service
systemctl enable cleanup.service
systemctl enable copytoserver@$Username.service
# systemctl enable config-server-api.service
# systemctl start config-server-api.service

# Set timezone
timedatectl set-timezone Europe/Amsterdam

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

export $Username
