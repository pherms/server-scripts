#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

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

if [ "${addRegularUser,,}" = "y" ]; then
  #add regular user
  useradd -m -s /bin/bash -p $(openssl passwd -crypt $password) -G sudo $userName
fi

# setup fstab
nvme=$(lsblk -d | grep nvme | awk '$1 !~ "loo|sd" {print $1}')
if [ -z "$nvme" ]; then
  echo "second disk found"
  echo "Creating mount point"
  mkdir -p /mnt/vmdisks
  echo "Mounting second disk"
  echo "/dev/$nvme  /mnt/vmdisks  xfs   defaults,relatime  0 0"
fi  

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

