#!/bin/bash
echo "Installeren van CA authority"
# Zie https://www.digitalocean.com/community/tutorials/how-to-set-up-and-configure-a-certificate-authority-ca-on-ubuntu-20-04

echo "Installeren van easy-rsa"
apt install -y easy-rsa

easyrsadir="~/easy-rsa"
echo "Creeeren van CA directory"
mkdir -p $easyrsadir

echo "Symlink maken"
ln -s /usr/share/easy-rsa/* $easyrsadir

echo "Vars file kopieeren"
cp ./roles/files/ca/vars /$easyrsadir

echo "Rechten zetten"
chmod 700 $easyrsadir

echo "Initialiseren van pki"
cd $easyrsadir
./easyrsa init-pki

echo "CA certificaat genereren"
./easyrsa build-ca nopass

./roles/firewall.sh $1