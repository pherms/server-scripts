#!/bin/bash

# $1: DHCP protocol version
function dhcpserver {
    dhcpProtocol = $1

    if [[ ! -f /etc/dhcp/dhcpd$dhcpProtocol.conf ]]; then
        echo "Copy config file"
        cp ./roles/files/system/dhcp4$dhcpProtocol.conf /etc/dhcp/
    fi

    echo "Setup DHCP service Units"
    if [[ ! -f /etc/systemd/system/dhcp-server$dhcpProtocol.service ]]; then
        echo "DHCP IPv$dhcpProtocol Unit"
        cp ./roles/files/system/dhcp-server$dhcpProtocol.service /etc/systemd/system/
        systemctl daemon-reload
        
        echo "DHCP server voor IPv$dhcpProtocol starten"
        dhcpstatus=$(systemctl show dhcp-server$dhcpProtocol --property=SubState | awk 'BEGIN{FS="="} {print $2}')
        if [[ "$dhcpstatus" != "running" ]]; then
            echo "Enable en start DHCP server IPv$dhcpProtocol"
            systemctl enable dhcp-server$dhcpProtocol.service
            systemctl start dhcp-server$dhcpProtocol.service
        else
            echo "DHCP server voor IPv$dhcpProtocol is al gestart"
        fi
    fi
}

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

# DHCP server
dhcpserver 4
dhcpserver 6

echo "Enable en start bind DNS server"
systemctl enable named
systemctl start named

./roles/firewall.sh $1