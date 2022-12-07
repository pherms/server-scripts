#!/bin/bash
#read -p "Welke rol krijgt deze server? (db,infra,proxy,web,docker,ventrilo,samba,smtp)? " role
role=$1
echo "Installeren nftables (firewall)"
apt update
apt install -y nftables

echo "Argument: $1"
echo "Geselecteerde rol: $role"
# switch statement rol
case $role in
db)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-db.sh
infra)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-infra.sh
proxy)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-proxy.sh
web)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-web.sh
docker)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-docker.sh
ventrilo)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-ventrilo.sh
smaba)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-smb.sh
smtp)
  ./fw-rules/firewall-base.sh
  ./fw-rules/firewall-smtp.sh
*)
echo "Rol niet gevonden. Script wordt afgebroken"
exit 1

esac

systemctl enable nftables.service
systemctl start nftables.service