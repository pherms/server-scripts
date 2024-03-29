#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

# Set hostname
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
hostnamectl set-hostname $hostname

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
  sed -i 's/main/main contrib non-free/' /etc/apt/sources.list
fi

apt update -y
apt install -y git sudo screenfetch intel-microcode initramfs-tools firmware-linux snapd lshw xfsprogs openssh-server prometheus-node-exporter dnsutils resolvconf rsync ntp acl python3 python3-pip python3-requests

# create backup directory
mkdir -p /vol/backup

# create config directory
mkdir -p /etc/server-scripts

# Kopieren van bestanden
yes | cp ./roles/files/system/resolv.conf /etc/
yes | cp ./roles/files/system/head /etc/resolvconf/resolv.conf.d/
yes | cp ./backup/systemd/* /etc/systemd/system/
yes | cp ./backup/config.json /etc/server-scripts/backup-config.json
yes | cp ./backup/sources /etc/server-scripts/

# reload systemctl daemon en enable en start services
systemctl daemon-reload
systemctl enable ssh.service
systemctl start ssh.service
systemctl enable prometheus-node-exporter.service
systemctl start prometheus-node-exporter.service
systemctl enable resolvconf.service
systemctl start resolvconf.service
systemctl restart systemd-resolved.service
systemctl enable backup.timer
systemctl start backup.timer
systemctl enable autoupdate.timer
systemctl start autoupdate.timer
systemctl enable backup.service
systemctl enable cleanup.service
systemctl enable copytoserver@$Username.service


# Set timezone
timedatectl set-timezone Europe/Amsterdam

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

export $Username
export $password
