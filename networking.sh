#!/bin/bash
installBridge=$1
nic=$(ip -br l | awk '$1 !~ "lo|vir|wl" { print $1}')
bridgeName="bridge0"

if [ "$installBridge" == "bridge" ]; then
  apt install -y bridge-utils
  brctl addbr $bridgeName
  brctl addif $bridgeName $nic
  systemctl restart networking
fi

apt install -y inetutils-ping
