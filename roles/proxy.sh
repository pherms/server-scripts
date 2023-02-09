#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Installing nginx"
apt update
apt install -y nginx nginx-doc curl wget gpg apt-transport-https 

echo "Toevoegen van elasticsearch key aan repository"
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

echo "Bijwerken sources list en bijwerken cache"
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt update

echo "Installeren van elastic-agent"
apt install -y metricbeat filebeat elastic-agent

echo "Start en enable nginx"
systemctl enable nginx
systemctl start nginx

echo "Disable default virtual host"
unlink /etc/nginx/sites-enabled/default

echo "Setup websites"
echo "Setup Kibana"
if [[ ! -f /etc/nginx/sites-available/kibana ]]; then
    cp ./roles/files/nginx/kibana /etc/nginx/sites-available/kibana
fi

echo "Geconfigureerde websites live zetten"
echo "Kibana..."
ln -s /etc/nginx/sites-available/kibana /etc/nginx/sites-enabled/kibana
status=$(nginx -t | awk '$1 !~ "syntax is ok" { print $1}')
if [[ "$status" = "syntax is ok" ]]; then
    echo "De Kibana webserver is juist geconfigureerd"
fi
#./roles/firewall.sh $1