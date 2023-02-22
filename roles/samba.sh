#!/bin/bash
# Functions
function GetPassword {
  read -p "Username: " userName
  read -sp "Password: " password1
  read -sp "Re-enter password: " password2
}

echo "Samba erver wordt geïnstalleerd"
apt install -y samba curl wget gpg apt-transport-https 

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
    echo "Passwords match"
    password=$password1
  else
    GetPassword
  fi
fi
echo -e "$password\n$password" | smbpasswd -a -s $username

./roles/firewall.sh $1