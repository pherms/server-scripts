#!/bin/bash
read -p "Welke rol krijgt deze server? (db,infra,proxy,web,docker,ventrilo)? " role
echo "Installeren nftables (firewall)"
apt update
apt install -y nftables

# adding default rule
echo "Standaard regels toevoegen"
if [[ -z "(nft list tables)" ]]; then
    nft add table inet firewall
    nft 'add chain ip firewall input { type filter hook input priority 0; policy drop ; }'
fi

if [[ -z "(nft list chains | grep input_ipv4)" ]]; then
    nft add chain ip firewall input_ipv4
fi

if [[ -z "(nft list chains | grep input_ipv6)" ]]; then
    nft add chain ip firewall input_ipv6
    nft add rule ip firewall input_ipv6 icmpv6 type { nd-neighbor-solicit, nd-router-advert, nd-neighbor-advert } accept
fi

if [[ -z "(nft list chains | grep 'input {')" ]]; then
    nft add rule ip firewall input tcp dport 22 ct state new,established counter accept
    nft add rule ip firewall input 'ct state vmap { established: accept, related: accept, invalid: drop }'
    nft add rule ip firewall input iifname lo accept
    nft add rule ip firewall input meta protocol vmap { ip : jump inbound_ipv4, ip6 : jump inbound_ipv6 }
fi

# switch statement rol
case $role in
db)
  mariadbInstalled=$(dpkg-query -l | grep mariadb-server | awk '$1 {print $2}' )
  postgresInstalled=$(dpkg-query -l | grep postgresql | awk '$1 {print $2}' )

  if [[ -n "mariadbInstalled" ]]; then
    echo "MariaDB server is installed setting up firewall rules"
    nft add rule inet firewall input tcp dport 3306 state new,established counter accept

infra)

proxy)

web)

docker)

ventrilo)

*)
echo "Rol niet gevonden. Script wordt afgebroken"
exit 1

esac

systemctl enable nftables.service
systemctl start nftables.service