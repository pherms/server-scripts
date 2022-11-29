#!/bin/bash
read installBridge="Install bridge or nic config?: "
read staticIp="Static IP address?: "

nic=$(ip -br l | awk '$1 !~ "lo|vir|wl" { print $1}')
bridgeName="bridge0"

if [ "$installBridge" == "bridge" ]; then
  apt install -y bridge-utils
  brctl addbr $bridgeName
  brctl addif $bridgeName $nic
  sed "s/iface $nic inet dhcp/# iface $nic inet dhcp/" /etc/network/interfaces
  sed "s/iface $nic inet auto/iface $nic inet manual/" /etc/network/interfaces
  echo "# Configure bridge" >> /etc/network/interfaces
  echo "iface $bridgeName inet static" >> /etc/network/interfaces
  echo "  bridge_ports $nic" >> /etc/network/interfaces
  echo "    address $staticIp/24" >> /etc/network/interfaces
  echo "    broadcast 192.168.2.255" >> /etc/network/interfaces
  echo "    gateway 192.168.2.1" >> /etc/network/interfaces
  echo "    network 192.168.2.0" >> /etc/network/interfaces
  systemctl restart networking
else
  echo "# Configure Network interface" >> /etc/network/interfaces
  echo "iface $nic inet static" >> /etc/network/interfaces
  echo "  address $staticIp/24" >> /etc/network/interfaces
  echo "  broadcast 192.168.2.255" >> /etc/network/interfaces
  echo "  gateway 192.168.2.1" >> /etc/network/interfaces
  echo "  network 192.168.2.0" >> /etc/network/interfaces
  systemctl restart networking
fi

apt install -y inetutils-ping
