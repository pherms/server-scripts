#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Installeren bind DNS en DHCP server"
apt update
apt install -y bind9 bind9-dnsutils bind9-doc bind9-host isc-dhcp-server curl wget gpg apt-transport-https 

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

if [[ ! -f /etc/systemd/system/dhcp-server4.service ]]; then
    echo "Setup DHCP service Units"
    echo "DHCP IPv4 Unit"
    echo "[Unit]" >> /etc/systemd/system/dhcp-server4.service
    echo "Description=ISC DHCP Server for IPv4 (dhcpd.conf)" >> /etc/systemd/system/dhcp-server4.service
    echo "Wants=network-online.target" >> /etc/systemd/system/dhcp-server4.service
    echo "After=network-online.target" >> /etc/systemd/system/dhcp-server4.service
    echo -en '\n' >> /etc/systemd/system/dhcp-server4.service
    echo "[Install]" >> /etc/systemd/system/dhcp-server4.service
    echo "WantedBy=multi-user.target" >> /etc/systemd/system/dhcp-server4.service
    echo -en '\n' >> /etc/systemd/system/dhcp-server4.service
    echo "[Service]" >> /etc/systemd/system/dhcp-server4.service
    echo "KillMode=mixed" >> /etc/systemd/system/dhcp-server4.service
    echo "Type=forking" >> /etc/systemd/system/dhcp-server4.service
    echo "PIDFile=/var/run/dhcpd.pid" >> /etc/systemd/system/dhcp-server4.service
    echo "ExecStartPre=/usr/bin/touch /var/lib/dhcp/dhcpd.leases" >> /etc/systemd/system/dhcp-server4.service
    echo "ExecStart=/usr/sbin/dhcpd -4 -q -cf /etc/dhcp/dhcpd.conf" >> /etc/systemd/system/dhcp-server4.service
    
    echo "Enable en start DHCP server IPv4"
    systemctl enable dhcp-server4.service
    systemctl start dhcp-server4.service
fi

if [[ ! -f /etc/systemd/system/dhcp-server6.service ]]; then
    echo "DHCP IPv6 Unit"
    echo "[Unit]" >> /etc/systemd/system/dhcp-server6.service
    echo "Description=ISC DHCP Server for IPv6 (dhcpd6.conf)" >> /etc/systemd/system/dhcp-server6.service
    echo "Wants=network-online.target" >> /etc/systemd/system/dhcp-server6.service
    echo "After=network-online.target" >> /etc/systemd/system/dhcp-server6.service
    echo -en '\n' >> /etc/systemd/system/dhcp-server6.service
    echo "[Install]" >> /etc/systemd/system/dhcp-server6.service
    echo "WantedBy=multi-user.target" >> /etc/systemd/system/dhcp-server6.service
    echo -en '\n' >> /etc/systemd/system/dhcp-server6.service
    echo "[Service]" >> /etc/systemd/system/dhcp-server6.service
    echo "KillMode=mixed" >> /etc/systemd/system/dhcp-server6.service
    echo "Type=forking" >> /etc/systemd/system/dhcp-server6.service
    echo "PIDFile=/var/run/dhcpd6.pid" >> /etc/systemd/system/dhcp-server6.service
    echo "ExecStartPre=/usr/bin/touch /var/lib/dhcp/dhcpd6.leases" >> /etc/systemd/system/dhcp-server6.service
    echo "ExecStart=/usr/sbin/dhcpd -6 -q -cf /etc/dhcp/dhcpd6.conf" >> /etc/systemd/system/dhcp-server6.service

    echo "Enable en start DHCP server IPv6"
    systemctl enable dhcp-server6.service
    systemctl start dhcp-server6.service
fi

echo "Enable en start bind DNS server"
systemctl enable named
systemctl start named

./roles/firewall.sh $1