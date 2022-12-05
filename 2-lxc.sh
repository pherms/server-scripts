#!/bin/bash
# install lxc
apt install lxc lxc-templates debootstrap libvirt0 libpam-cgfs bridge-utils uidmap libvirt-clients libvirt-daemon-system iptables ebtables dnsmasq-base libxml2-utils iproute2 cgroupfs-mount -y --no-install-recommends
snap install lxd

bridge=$(ip -br l | awk '$1 !~ "lo|vir|wl|enp" { print $1}')

# update /etc/lxc/default.conf
echo "Updating /etc/lxc/default.conf file"
#echo "Writing /etc/lxc/default.conf"
#echo "lxc.net.0.type = veth" > /etc/lxc/default.conf
#echo "lxc.net.0.link = $bridge" >> /etc/lxc/default.conf
#echo "lxc.net.0.flags = up" >> /etc/lxc/default.conf
#echo "" >> /etc/lxc/default.conf
#echo "lxc.apparmor.profile = generated" >> /etc/lxc/default.conf
#echo "lxc.apparmor.allow_nesting = 1" >> /etc/lxc/default.conf

# disable virtual bridge
echo "Disable virtual bridge"
sed -i 's/USE_LXC_BRIDGE="true"/USE_LXC_BRIDGE="false"/' /etc/default/lxc-net

# start virsh
echo "Starting virtual network"
virsh net-start default
virsh net-autostart default

# update sysctl
echo "Checking sysctl config"
SYSCTL=$( sysctl kernel.unprivileged_userns_clone )
unprivEnabled=${SYSCTL: -1}
if [ $unprivEnabled = 0 ]; then
    echo "kernel.unprivileged_userns_clone=1" > /etc/sysctl.d/unpriv-usernd.conf
    sysctl -p
fi

# allow admin user to create virtual network interfaces
echo "Allow user to create asdditional vNICs"
echo admin veth lxcbr0 10 >> /etc/lxc/lxc-usernet

# make cgroup systemd mount
echo "Create directory for cgroup systemd mount"
cgroupDir="/sys/fs/cgroup/systemd"
mkdir -p $cgroupDir
mount -t cgroup -o none,name=systemd systemd $cgroupDir

logout