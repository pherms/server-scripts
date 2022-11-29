#!/bin/bash
read -p "Install bridge or nic config?: " installBridge
read -p "Static IP address?: " staticIp

nic=$(ip -br l | awk '$1 !~ "lo|vir|wl|bridge0" { print $1}')
bridgeName="bridge0"

if [ "$installBridge" == "bridge" ];
then
  apt install -y bridge-utils
  brctl addbr $bridgeName
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
else
  echo "# Configure Network interface" >> /etc/network/interfaces
  echo "iface $nic inet static" >> /etc/network/interfaces
  echo "  address $staticIp/24" >> /etc/network/interfaces
  echo "  broadcast 192.168.2.255" >> /etc/network/interfaces
  echo "  gateway 192.168.2.1" >> /etc/network/interfaces
  echo "  network 192.168.2.0" >> /etc/network/interfaces
  echo "# Configure IPv6 interface" >> /etc/network/interfaces
  echo "iface $nic inet6 dhcp" >> /etc/network/interfaces
  systemctl restart networking
fi

apt install -y inetutils-ping
