#!/bin/bash
read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Webserver apache wordt geïnstalleerd"
apt install -y apache apt-transport-https lsb-release ca-certificates curl php php-mysql libapache2-mod-php php-curl php-cli php-gd php-common php-xml php-json php-intl php-pear php-imagick php-dev php-common php-mbstring php-zip php-soap php-bz2 php-bcmath php-gmp php-apcu
apt install -y libmagickcore-dev unzip certbot

echo "Activeren apache modules"
a2enmod status rewrite ssl headers

echo "Configureren php voor Nextcloud"
sed -i 's/^file_uploads = .*/On/' /etc/php/7.4/apache2/php.ini
sed -i 's/^allow_url_fopen = .*/On/' /etc/php/7.4/apache2/php.ini
sed -i 's/^memory_limit = .*/512M/' /etc/php/7.4/apache2/php.ini
sed -i 's/^upload_max_filesize = .*/500M/' /etc/php/7.4/apache2/php.ini
sed -i 's/^post_max_size = .*/600M/' /etc/php/7.4/apache2/php.ini
sed -i 's/^max_execution_time = .*/300/' /etc/php/7.4/apache2/php.ini
sed -i 's/^display_errors = .*/Off/' /etc/php/7.4/apache2/php.ini
sed -i 's/^date.timezone = .*/Europe\/Amsterdam/' /etc/php/7.4/apache2/php.ini
sed -i 's/^foutput_buffering = .*/Off/' /etc/php/7.4/apache2/php.ini

echo "opcache.enable = 1" >> /etc/php/7.4/apache2/php.ini
echo "opcache.interned_strings_buffer = 8" >> /etc/php/7.4/apache2/php.ini
echo "opcache.max_accelerated_files = 10000" >> /etc/php/7.4/apache2/php.ini
echo "opcache.memory_consumption = 128" >> /etc/php/7.4/apache2/php.ini
echo "opcache.save_comments = 1" >> /etc/php/7.4/apache2/php.ini
echo "opcache.revalidate_freq = 1" >> /etc/php/7.4/apache2/php.ini

echo "Apache2 service herstarten"
systemctl restart apache2

echo "Downloaden en installeren van NextCloud"
cd /var/www/
curl -o nextcloud.zip https://download.nextcloud.com/server/releases/nextcloud-25.0.2.zip
unzip nextcloud.zip
chown -R www-data:www-data nextcloud
rm nextcloud.zip

echo "Setup Letsencrypt certbot"
mkdir -p /var/lib/letsencrypt/.well-known
chgrp www-data /var/lib/letsencrypt
chmod g+s /var/lib/letsencrypt

echo "Schrijven van well-known.conf bestand"
cd /etc/apache2/conf-available/

echo "Alias /.well-known/acme-challenge/ \"/var/lib/letsencrypt/.well-known/acme-challenge/\"" >> well-known.conf
echo "<Directory \"/var/lib/letsencrypt/\">" >> well-known.conf
echo "    AllowOverride None" >> well-known.conf
echo "    Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec" >> well-known.conf
echo "    Require method GET POST OPTIONS" >> well-known.conf
echo "</Directory>" >> well-known.conf

echo "Indien configuratie geen fouten bevat, dan herstarten"
configOk=$(apachectl configtest)
if [[ "$configOk" == "Syntax OK" ]]; then
  systemctl restart apache2
fi

echo "Downloaden en installeren van wordpress"
cd /var/www/
curl -o wordpress.tar.gz https://wordpress.org/latest.tar.gz
tar -xzvf wordpress.tar.gz
chown -R www-data:www-data wordpress
rm wordpress.tar.gz

echo "Downloaden en installeren PhpMyAdmin"
curl -o phpmyadmin.tar.gz https://www.phpmyadmin.net/downloads/phpMyAdmin-latest-all-languages.tar.gz
tar -xzvf phpmyadmin.tar.gz
chown -R www-data:www-data phpmyadmin
rm phpmyadmin

echo "Bijwerken firewall regels"
#./roles/firewall.sh $1