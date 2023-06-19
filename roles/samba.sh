#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

echo "Hostame ophalen"
hostname=$(cat /etc/hostname)

echo "Samba erver wordt geïnstalleerd"
apt install -y samba curl wget gpg apt-transport-https acl

echo "Gebruiksaccount toevoegen. Dit is hetzelfde account als in base install is aangemaakt"

# Setup regular user
read -p "Normale gebruiker toevoegen? (Y/N): " addSambaUser
read -p "Geef gebruikersnaam van de gebruiker: " sambaUser

if [[ "${addSambaUser,,}" = "y" ]]; then
  smbpasswd -a $sambaUser -n
  GetPassword
  if [[ "$password1" = "$password2" ]]; then
    echo "Passwords match"
    password=$password1
  else
    GetPassword
  fi
fi
echo -e "$password\n$password" | smbpasswd -a -s $username

echo "Samba groep aanmaken"
groupadd samba-fs

echo "Users toevoegen aan Samba groep"
usermod -aG samba-fs pascal

echo "Configureren samba share"

if [[ ! -d /vol/fs/samba-fs ]]; then
  mkdir -p /vol/fs/samba-fs
fi

echo "Samba-fs share configureren"

echo "[samba-fs]" >> /etc/samba/smb.conf
echo "  comment = Windows fileshare on $hostname" >> /etc/samba/smb.conf
echo "  path = /vol/fs/samba-fs" >> /etc/samba/smb.conf
echo "  read-only = no" >> /etc/samba/smb.conf
echo "  writable = yes" >> /etc/samba/smb.conf
echo "  browsable = yes" >> /etc/samba/smb.conf
echo "  valid users = @samba-fs" >> /etc/samba/smb.conf

echo "Controleren of nmbd service is gestart"
isNmbdRunning=$(systemctl status nmbd | grep '(running)')

if [[ -z $isNmbdRunning ]]; then
  systemctl start nmbd
  systemctl enable nmbd
fi

./roles/firewall.sh $1