#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

function startBeats {
  # $1: type agent (filebeat of metricbeat)
  agentType=$1
  configPath="/etc/$agentType"

  if [[ -d /etc/${agentType} ]]; then
    echo "Kopieren $agentType config file"
    if [[ -f ${configPath}/${agentType}.yml ]]; then
      yes | cp ./roles/files/system/${agentType}.yml ${configPath}/
    fi
  fi
  systemctl enable agentType
  systemctl start agentType
}

# Set hostname
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

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
  useradd -m -s /bin/bash -p $(openssl passwd -crypt $password) -G sudo $userName
fi

# update sources-list
isContrib=$(grep "main contrib non-free" /etc/apt/sources.list)
if [[ -z "$isContrib" ]]; then
  echo "non-free repos not enabled; enabling..."
  sed -i 's/main/main contrib non-free/' /etc/apt/sources.list
fi

apt update -y
apt install -y git sudo screenfetch intel-microcode initramfs-tools firmware-linux snapd lshw xfsprogs openssh-server

systemctl enable ssh.service
systemctl start ssh.service

echo "Toevoegen van elasticsearch key aan repository"
if [[ ! -f /usr/share/keyrings/elasticsearch-keyring.gpg ]]; then
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
fi

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

startBeats metricbeat
startBeats filebeat

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

export $Username
export $password
