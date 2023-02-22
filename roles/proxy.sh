#!/bin/bash
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
echo "Kibana"
if [[ ! -f /etc/nginx/sites-available/kibana ]]; then
    cp ./roles/files/nginx/kibana /etc/nginx/sites-available/kibana
    echo "Website Kibana live zetten..."
    ln -s /etc/nginx/sites-available/kibana /etc/nginx/sites-enabled/kibana
fi

echo "Nextcloud"
if [[ ! -f /etc/nginx/sites-available/cloud ]]; then
    cp ./roles/files/nginx/cloud /etc/nginx/sites-available/cloud
    echo "Website Nextcloud live zetten..."
    ln -s /etc/nginx/sites-available/cloud /etc/nginx/sites-enabled/cloud
fi

echo "wordpress"
if [[ ! -f /etc/nginx/sites-available/www ]]; then
    cp ./roles/files/nginx/www /etc/nginx/sites-available/www
    echo "Website wordpress live zetten..."
    ln -s /etc/nginx/sites-available/www /etc/nginx/sites-enabled/www
fi

echo "Bookstack"
if [[ ! -f /etc/nginx/sites-available/docs ]]; then
    cp ./roles/files/nginx/docs /etc/nginx/sites-available/docs
    echo "Website docs live zetten..."
    ln -s /etc/nginx/sites-available/docs /etc/nginx/sites-enabled/docs
fi

status=$(nginx -t | awk '$1 !~ "syntax is ok" { print $1}')
if [[ "$status" = "syntax is ok" ]]; then
    echo "Nginx is juist geconfigureerd. Restarting..."
    systemctl restart nginx
fi

./roles/firewall.sh $1