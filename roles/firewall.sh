#!/bin/bash
#read -p "Welke rol krijgt deze server? (db,infra,proxy,web,docker,ventrilo,samba,smtp,kibana)? " role
role=$1
echo "Installeren nftables (firewall)"
apt update
apt install -y nftables

systemctl enable nftables.service
systemctl start nftables.service

echo "Geselecteerde rol: $role"
# switch statement rol
case $role in
    ca)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-ca.sh
      ;;
    db)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-db.sh
      ;;
    infra)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-infra.sh
      ;;
    kibana)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-kibana.sh
      ;;
    proxy)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-proxy.sh
      ;;
    web)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-web.sh
      ;;
    docker)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-docker.sh
      ;;
    samba)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-smb.sh
      ;;
    smtp)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-smtp.sh
      ;;
    kubernetes)
      echo "Installeren basis firewall regel set"
      ./roles/fw-rules/firewall-base.sh
      echo "Installeren $role specifieke regel set"
      ./roles/fw-rules/firewall-kubernetes.sh
      ;;
    *)
      echo "Rol niet gevonden. Script wordt afgebroken"
      exit 1
      ;;
esac

echo "Opslaan van de ruleset in /etc/nftables.conf"
mv /etc/nftables.conf /etc/nftables.conf.empty
nft list ruleset >> /etc/nftables.conf
