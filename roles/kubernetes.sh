#!/bin/bash
echo "Opvragen hostname"
hostname=$(cat /etc/hostname)

echo "Gevonden hostname: $hostname"

./roles/firewall.sh $1