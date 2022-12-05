#!/bin/bash
echo "Setup UID en GID mapping for unprivileged containers"
echo "root:1000000:1000000000" | sudo tee -a /etc/subuid /etc/subgid

echo "Initial lxd setup"
echo "use existing bridge"
lxd init

echo "Create storage"
lxc storage create vm-storage dir source=/mnt/vmdisks/vm-storage
