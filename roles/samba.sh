#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Samba erver wordt geïnstalleerd"
apt install -y samba curl wget gpg apt-transport-https 

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

echo "Controleren of nmbd service is gestart"
isNmbdRunning=$(systemctl status nmbd | grep '(running)')

if [[ -z $isNmbdRunning ]]; then
  systemctl start nmbd
  systemctl enable nmbd
fi

echo "Gebruiksaccount toevoegen. Dit is hetzelfde account als in base install is aangemaakt"


# Setup regular user
read -p "Normale gebruiker toevoegen? (Y/N): " addSambaUser
if [[ "${addSambaUser,,}" = "y" ]]; then
  GetPassword
  if [[ "$password1" = "$password2" ]]; then
    echo "Passwords do match"
    password=$password1
  else
    GetPassword
  fi
fi
echo -e "$password\n$password" | smbpasswd -a -s $username

#./roles/firewall.sh $1