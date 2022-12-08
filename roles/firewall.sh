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
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-db.sh
      ;;
    infra)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-infra.sh
      ;;
    proxy)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-proxy.sh
      ;;
    web)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-web.sh
      ;;
    docker)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-docker.sh
      ;;
    smaba)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-smb.sh
      ;;
    smtp)
      ./roles/fw-rules/firewall-base.sh
      ./roles/fw-rules/firewall-smtp.sh
      ;;
    *)
      echo "Rol niet gevonden. Script wordt afgebroken"
      exit 1
      ;;
esac

systemctl enable nftables.service
systemctl start nftables.service