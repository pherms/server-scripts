#!/bin/bash
echo "Mailserver wordt geïnstalleerd"
echo "Installeren packages"

apt install -y postfix openssl mailx curl wget gpg apt-transport-https 

echo "Writing postfix configuration"
echo "smtpd_recipient_restrictions = reject_invalid_hostname, reject_unknown_recipient_domain, reject_unauth_destination, reject_rbl_client sbl.spamhaus.org, permit" >> /etc/postfix/main.cf
echo "smtpd_helo_restrictions = reject_invalid_helo_hostname, reject_non_fqdn_helo_hostname, reject_unknown_helo_hostname" >> /etc/postfix/main.cf

sed -i 's/^mydestination = .*/$hostname.merel107.local, merel107.local, $hostname.merel107.local, localhost.merel107.local, localhost/' /etc/postfix/main.cf
sed -i 's/^relayhost = .*/[smtp.kpnmail.nl]:587/' /etc/postfix/main.cf
sed -i 's/^smtp_sasl_auth_enable = .*/yes/' /etc/postfix/main.cf
sed -i 's/^smtp_sasl_password_maps = .*/hash:/etc/postfix/sasl_passwd/' /etc/postfix/main.cf
sed -i 's/^smtp_use_tls = .*/yes/' /etc/postfix/main.cf
sed -i 's/^smtp_tls_cert_file = .*//etc/pki/tls/certs/public.cert/' /etc/postfix/main.cf

echo "Postfix is geconfigureerd"
echo "Start en enable postfix service"

systemctl enable postfix
systemctl start postfix

./roles/firewall.sh $1