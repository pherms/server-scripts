#!/bin/bash
echo "Installeren van CA authority"
# Zie https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-a-certificate-authority-ca-on-ubuntu-20-04

echo "Installeren van easy-rsa"
apt install -y easy-rsa

easyrsadir="/var/lib/easy-rsa"
echo "Creeeren van CA directory"
sudo -u pascal mkdir -p $easyrsadir

echo "Symlink maken"
sudo -u pascal ln -s /usr/share/easy-rsa/* $easyrsadir

echo "Rechten zetten"
sudo -u pascal chmod 700 $easyrsadir

echo "Initialiseren van pki"
sudo -u pascal cd $easyrsadir
sudo -u pascal ./easyrsa init-pki
sudo -u pascal cp ./roles/files/ca/ca /$easyrsadir

echo "CA certificaat genereren"
sudo -u pascal ./easyrsa build-ca nopass

./roles/firewall.sh $1