#!/bin/bash
role=$1
shopt -s nocaseglob

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

read -p "Wat is de hostnaam van deze server?: " hostname
echo "Setting hostname"
echo $hostname >> /etc/hostname

echo "Webserver apache wordt geïnstalleerd"
apt install -y apache2 apt-transport-https lsb-release ca-certificates curl php php-mysql libapache2-mod-php php-curl php-cli php-gd php-common php-xml php-json php-intl php-pear php-imagick php-dev php-common php-mbstring php-zip php-soap php-bz2 php-bcmath php-gmp php-apcu
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
nextcloudSourceFile="nextcloud.zip"
nextcloudDir="nextcloud"
nextcloudUrl="https://download.nextcloud.com/server/releases/nextcloud-25.0.2.zip"
downloadExtract $nextcloudSourceFile $nextcloudDir $nextcloudUrl
# curl -o $nextcloudSourceFile https://download.nextcloud.com/server/releases/nextcloud-25.0.2.zip
# unzip -q $nextcloudSourceFile
# phpExtractDir=$(ls -d *next*)

# if [[ -n "$phpExtractDir" ]]; then
#   chown -R www-data:www-data nextcloud
#   rm nextcloud.zip
#   echo "Downloaden en uitpakken van Nextcloud is voltooid"
# fi

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
wordpressSourceFile="wordpress.tar.gz"
wordpressDir="wordpress"
wordpressUrl="https://wordpress.org/latest.tar.gz"
downloadExtract $wordpressSourceFile $wordpressDir $wordpressUrl
# curl -o $wordpressSourceFile https://wordpress.org/latest.tar.gz
# tar -xzf $wordpressSourceFile
# phpExtractDir=$(ls -d *wordpress*)

# if [[ -n "$phpExtractDir" ]]; then
#   chown -R www-data:www-data $wordpressDir
#   rm $wordpressSourceFile
#   echo "Downloaden en uitpakken van wordpress is voltooid"
# fi

echo "Downloaden en installeren PhpMyAdmin"
phpmyadminSourceFile="phpmyadmin.tar.gz"
phpmyadminDir="phpmyadmin"
phpmyadminUrl="https://files.phpmyadmin.net/phpMyAdmin/5.2.0/phpMyAdmin-5.2.0-english.tar.gz"
downloadExtract $phpmyadminSourceFile $phpmyadminDir $phpmyadminUrl
# curl -o $phpmyadminSourceFile https://files.phpmyadmin.net/phpMyAdmin/5.2.0/phpMyAdmin-5.2.0-english.tar.gz
# tar -xzf $phpmyadminSourceFile
# phpExtractDir=$(ls -d *php*)

# if [[ -n "$phpExtractDir" ]]; then
#   mv $phpExtractDir $phpmyadminDir
#   chown -R www-data:www-data $phpmyadminDir
#   rm $phpmyadminSourceFile
#   echo "Downloaden en uitpakken van phpmyadmin is voltooid"
# fi

./roles/firewall.sh $role