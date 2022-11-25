#!/bin/bash
# install lxc
apt install lxc libvirt0 libpam-cgfs bridge-utils uidmap libvirt-clients libvirt-daemon-system iptables ebtables dnsmasq-base libxml2-utils iproute2 -y --no-install-recommends

# update /etc/lxc/default.conf
echo "lxc.net.0.type = veth" > /etc/lxc/default.conf
echo "lxc.net.0.link = virbr0" >> /etc/lxc/default.conf
echo "lxc.net.0.flags = up" >> /etc/lxc/default.conf
echo "" >> /etc/lxc/default.conf
echo "lxc.apparmor.profile = generated" >> /etc/lxc/default.conf
echo "lxc.apparmor.allow_nesting = 1" >> /etc/lxc/default.conf

# start virsh
virsh net-start default
virsh net-autostart default

# update sysctl
SYSCTL=$( sysctl kernel.unprivileged_userns_clone )
unprivEnabled=${SYSCTL: -1}
if [ $unprivEnabled = 0 ]; then
    echo "kernel.unprivileged_userns_clone=1" > /etc/sysctl.d/unpriv-usernd.conf
    sysctl -p
fi

# allow admin user to create virtual network interfaces
echo admin veth lxcbr0 10 >> /etc/lxc/lxc-usernet
