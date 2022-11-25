#!/bin/bash
apt update -y
apt install screenfetch linux-firmware -y

# add regular user
useradd -G sudo admin
passwd admin

# configure screenfetch
echo "if [ -f /usr/bin/screenfetch ]; then" >> /etc/profile
echo "    screenfetch;" >> /etc/profile
echo "fi" >> /etc/profile

