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
echo "Setting hostname"
hostnamectl set-hostname $hostname

serverapidir="/opt/server-api/"
clientconfigdir="/var/www/client-config/"

# Setup regular user
read -p "Normale gebruiker toevoegen? (Y/N): " addRegularUser
if [[ "${addRegularUser,,}" = "y" ]]; then
  GetPassword
  if [[ "$password1" = "$password2" ]]; then
    echo "Passwords do match"
    password=$password1
  else
    GetPassword
  fi
fi

if [ "${addRegularUser,,}" = "y" ]; then
  #add regular user
  useradd -m -s /bin/bash -p $(openssl passwd -crypt $password) -G sudo,backup $userName
fi

# update sources-list
isContrib=$(grep "main contrib non-free" /etc/apt/sources.list)
if [[ -z "$isContrib" ]]; then
  echo "non-free repos not enabled; enabling..."
  sed -i 's/main/main non-free-firmware/' /etc/apt/sources.list
fi

apt update -y
apt install -y git sudo screenfetch intel-microcode initramfs-tools firmware-linux lshw openssh-server prometheus-node-exporter dnsutils systemd-resolved rsync ntp acl python3 python3-pip python3-requests nodejs apache2 postgresql-client

# create backup directory
mkdir -p /vol/backup

# create config directory
mkdir -p /etc/server-scripts

# create server-api directory
mkdir -p $serverapidir

# create config client directory
mkdir -p $clientconfigdir

if [[ ! "$( psql -h web01.hoofdspoor.home -XtAc "SELECT 1 FROM pg_database WHERE datname='DB_NAME'" )" = '1' ]]; then
  # run npx prisma command
  npx prisma migrate deploy
fi

# compile en copy api-server naar folder
cd /scripts/server-scripts/config/server
npm build

yes | cp -R dist/ $serverapidir
yes | cp src/controllers/authorization.controller.js ${serverapidir}controllers/
yes | cp src/middlewares/authorization/*.js ${serverapidir}middlewares/authorization/
yes | cp src/utils/helperfunctions.js ${serverapidir}utils/

# compile en copy client naar folder
cd /scripts/server-scripts/config/client
npm build
yes | cp -R dist/ $clientconfigdir
cp /scripts/server-scripts/roles/files/apache/config.conf /etc/apache2/sites-available/
a2ensite config.conf

# Kopieren van bestanden
# yes | cp ./roles/files/system/resolv.conf /etc/
# yes | cp ./roles/files/system/head /etc/resolvconf/resolv.conf.d/
yes | cp ./backup/systemd/* /etc/systemd/system/
yes | cp ./backup/config.json /etc/server-scripts/backup-config.json
yes | cp ./backup/sources /etc/server-scripts/

# Configure DNS
# resolvectl dns ens18 $dnsserver
# resolvectl domain ens18 $domainname

# reload systemctl daemon en enable en start services
systemctl daemon-reload
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
systemctl enable config-server-api.service
systemctl start config-server-api.service


# Set timezone
timedatectl set-timezone Europe/Amsterdam

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

export $Username
