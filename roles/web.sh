#!/bin/bash
role=$1
shopt -s nocaseglob

echo "De firewall rules aanmaken voor: $role"
./roles/firewall.sh $role

function downloadExtract {
  # $1: Source zip file, ie nextcloud.zip
  # $2: Program dir, i.e nextcloud
  # $3: URL

  echo "Downloaden $1"
  curl -o $1 $3
  filename=$(ls -p | grep -v /)
  IFS="." read -ra EXTENSION <<< "$filename"
  length=$(echo "${#EXTENSION[@]}")
  extension="${EXTENSION[$length-1]}"

  case $extension in
    gz)
    echo "Uitpakken $1"
    tar -xzf $1
    rm $1
    ;;
    zip)
    echo "Uitpakken $1"
    unzip -q $1
    rm $1
    ;;
  esac

  extractDir=$(ls -d *$2*)

  if [[ "$extractDir" != "$2" ]]; then
    echo "Verplaatsen van $extractDir naar $2"
    mv $extractDir $2/
  fi

  if [[ -d "$2" ]]; then
    chown -R www-data:www-data $2
    echo "Downloaden en uitpakken van $1 is voltooid"
  fi
}

function restartApache2 {
  echo "Indien configuratie geen fouten bevat, dan herstarten"
  configOk=$(apachectl configtest)
  if [[ "$configOk" == "Syntax OK" ]]; then
    systemctl restart apache2
  fi
}

phpVersion="7.4"

echo "Webserver apache wordt geïnstalleerd"
apt install -y apache2 apt-transport-https lsb-release ca-certificates curl php php-mysql libapache2-mod-php php-curl php-cli php-gd php-common php-xml php-json php-intl php-pear php-imagick php-dev php-common php-mbstring php-zip php-soap php-bz2 php-bcmath php-gmp php-apcu git composer
apt install -y libmagickcore-dev unzip certbot curl wget gpg apt-transport-https 

echo "Activeren apache modules"
a2enmod status rewrite ssl headers

echo "Configureren php voor Nextcloud"
sed -i 's/^file_uploads = .*/On/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^allow_url_fopen = .*/On/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^memory_limit = .*/512M/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^upload_max_filesize = .*/500M/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^post_max_size = .*/600M/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^max_execution_time = .*/300/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^display_errors = .*/Off/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^date.timezone = .*/Europe\/Amsterdam/' /etc/php/$phpVersion/apache2/php.ini
sed -i 's/^foutput_buffering = .*/Off/' /etc/php/$phpVersion/apache2/php.ini

echo "opcache.enable = 1" >> /etc/php/$phpVersion/apache2/php.ini
echo "opcache.interned_strings_buffer = 8" >> /etc/php/$phpVersion/apache2/php.ini
echo "opcache.max_accelerated_files = 10000" >> /etc/php/$phpVersion/apache2/php.ini
echo "opcache.memory_consumption = 128" >> /etc/php/$phpVersion/apache2/php.ini
echo "opcache.save_comments = 1" >> /etc/php/$phpVersion/apache2/php.ini
echo "opcache.revalidate_freq = 1" >> /etc/php/$phpVersion/apache2/php.ini

echo "Apache2 service herstarten"
systemctl restart apache2

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

restartApache2

echo "Setup webserver apache voltooid. Installeren webapps."
echo "Downloaden en installeren van NextCloud"
cd /var/www/
nextcloudSourceFile="nextcloud.zip"
nextcloudDir="nextcloud"
nextcloudUrl="https://download.nextcloud.com/server/releases/nextcloud-25.0.2.zip"
downloadExtract $nextcloudSourceFile $nextcloudDir $nextcloudUrl
echo "Kopiëren van nextcloud apache2 config file"
if [[ ! -f /etc/apache2/sites-available/cloud.conf ]]; then
    cp ./roles/files/apache/cloud.conf /etc/apache2/sites-available/coud.conf
fi

echo "Downloaden en installeren van wordpress"
cd /var/www/
wordpressSourceFile="wordpress.tar.gz"
wordpressDir="wordpress"
wordpressUrl="https://wordpress.org/latest.tar.gz"
downloadExtract $wordpressSourceFile $wordpressDir $wordpressUrl
echo "Kopiëren van wordpress apache2 config file"
if [[ ! -f /etc/apache2/sites-available/www.conf ]]; then
    cp ./roles/files/apache/www.conf /etc/apache2/sites-available/www.conf
fi

echo "Installeer Bookstack handmatig. Zie url: https://www.bookstackapp.com/docs/admin/installation/"
echo "Kopiëren van Bookstack apache2 config file"
if [[ ! -f /etc/apache2/sites-available/docs.conf ]]; then
    cp ./roles/files/apache/docs.conf /etc/apache2/sites-available/docs.conf
fi

echo "Downloaden en installeren PhpMyAdmin"
phpmyadminSourceFile="phpmyadmin.tar.gz"
phpmyadminDir="phpmyadmin"
phpmyadminUrl="https://files.phpmyadmin.net/phpMyAdmin/5.2.0/phpMyAdmin-5.2.0-english.tar.gz"
downloadExtract $phpmyadminSourceFile $phpmyadminDir $phpmyadminUrl

echo "Verwijderen default site"
defaultSite=$(a2query -s | awk '$1 ~ "000-default" { print $1}')
if [[ "$defaultSite" = "000-default" ]]; then
  echo "Default site is actief. Uitschakelen."
  a2dissite $defaultSite
fi

a2dissite 000-default
if [[ -d /var/www/html ]]; then
  rm -rf /var/www/html
fi

echo "Apache2 configuratie verversen"
systemctl reload apache2

shopt -u nocaseglob

restartApache2

# firewall rules verplaatst naar top van het script