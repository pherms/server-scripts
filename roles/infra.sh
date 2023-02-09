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

echo "Setup DHCP service Units"
if [[ ! -f /etc/systemd/system/dhcp-server4.service ]]; then
    echo "DHCP IPv4 Unit"
    cp ./roles/files/system/dhcp-server4.service /etc/systemd/system/
    systemctl daemon-reload
    
    echo "DHCP server voor IPv4 starten"
    dhcp4status=$(systemctl show dhcp-server4 --property=SubState | awk 'BEGIN{FS="="} {print $2}')
    if [[ "$dhcp4status" != "running" ]]; then
        echo "Enable en start DHCP server IPv4"
        systemctl enable dhcp-server4.service
        systemctl start dhcp-server4.service
    else
        echo "DHCP server voor IPv4 is al gestart"
    fi
fi

if [[ ! -f /etc/systemd/system/dhcp-server6.service ]]; then
    echo "DHCP IPv6 Unit"
    cp ./roles/files/system/dhcp-server6.service /etc/systemd/system/
    systemctl daemon-reload
    
    dhcp6status=$(systemctl show dhcp-server6 --property=SubState | awk 'BEGIN{FS="="} {print $2}')
    if [[ "$dhcp6status" != "running" ]]; then
        echo "Enable en start DHCP server IPv6"
        systemctl enable dhcp-server6.service
        systemctl start dhcp-server6.service
    else
        echo "DHCP server voor IPv6 is al gestart"
    fi
fi

echo "Enable en start bind DNS server"
systemctl enable named
systemctl start named

./roles/firewall.sh $1