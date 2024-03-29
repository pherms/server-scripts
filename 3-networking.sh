#!/bin/bash
read -p "Install bridge or nic config?: " installBridge
if [ "$installBridge" == "bridge" ]; then
  read -p "Static IP address?: " staticIp
fi

read -p "Welke rol (Cert(A)uthority, (I)nfra,(D)b,(W)eb,(P)roxy,Do(C)ker,(M)ail,(S)amba,(K)ibana),K(U)bernetes krijgt deze machine?: " role

nic=$(ip -br l | awk '$1 !~ "lo|vir|wl|br0|lxc" { print $1}')
bridgeName=$(ip -br l | awk '$1 !~ "lo|vir|wl|enp" { print $1}')

backupfolder=/vol/backup
logfolder=/home/$Username/log

# create backup directory
if [[ ! -d $backupfolder ]]:
  mkdir -p $backupfolder
fi

# create backup directory
if [[ ! -d $logfolder ]]:
  mkdir -p $logfolder
fi

# Update acl
setfacl -R -m g:backup:rwX $backupfolder
setfacl -R -m u:Username:rwX $logfolder

if [ "$installBridge" == "bridge" ];
then
  apt install -y bridge-utils
  if [[ -z "$bridgeName" ]]; then
    brctl addbr $bridgeName
  fi
  brctl addif $bridgeName $nic
  echo $nic
  sed -i 's/iface '"$(echo ${nic})"' inet dhcp/# iface '"$(echo ${nic})"' inet dhcp/' /etc/network/interfaces
  sed -i 's/allow-hotplug '"$(echo ${nic})"'/# allow-hotplug '"$(echo ${nic})"'/' /etc/network/interfaces
  sed -i 's/iface '"$(echo ${nic})"' inet6 dhcp/# iface '"$(echo ${nic})"' inet6 dhcp/' /etc/network/interfaces
  sed -i 's/iface '"$(echo ${nic})"' inet6 auto/# iface '"$(echo ${nic})"' inet6 auto/' /etc/network/interfaces
  sed -i 's/iface '"$(echo ${nic})"' inet auto/# iface '"$(echo ${nic})"' inet auto/' /etc/network/interfaces
  echo "# Configure bridge" >> /etc/network/interfaces
  echo "auto $bridgeName" >> /etc/network/interfaces
  echo "iface $bridgeName inet static" >> /etc/network/interfaces
  echo "  address $staticIp/24" >> /etc/network/interfaces
  echo "  broadcast 192.168.2.255" >> /etc/network/interfaces
  echo "  gateway 192.168.2.1" >> /etc/network/interfaces
  echo "  network 192.168.2.0" >> /etc/network/interfaces
  echo "  bridge_ports $nic" >> /etc/network/interfaces
  echo "  bridge_stp off" >> /etc/network/interfaces
  echo "    bridge_waitport 0" >> /etc/network/interfaces
  echo "    bridge_fd 0" >> /etc/network/interfaces
  echo " " >> /etc/network/interfaces
  echo "# Configure IPv6 on bridge" >> /etc/network/interfaces
  echo "iface $bridgeName inet6 dhcp" >> /etc/network/interfaces
  echo "  bridge_ports $nic" >> /etc/network/interfaces
  systemctl restart networking
fi

apt install -y inetutils-ping

selectedRole="${role,,}"
case $selectedRole in
  a)
  ./roles/ca.sh ca
  ;;
  c)
  ./roles/docker.sh docker
  ;;
  d)
  ./roles/database.sh db
  ;;
  i)
  ./roles/infra.sh infra
  ;;
  k)
  ./roles/kibana.sh kibana
  ;;
  m)
  ./roles/mail.sh smtp
  ;;
  p)
  ./roles/proxy.sh proxy
  ;;
  s)
  ./roles/samba.sh samba
  ;;
  u)
  ./roles/kubernetes.sh kubernetes
  ;;
  w)
  ./roles/web.sh web
  ;;
  *)
  echo "Geen geldige keuze. Script wordt afgebroken"
  exit 1
esac