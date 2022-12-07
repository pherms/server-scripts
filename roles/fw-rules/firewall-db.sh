#!/usr/sbin/nft -f

# Mysql
add rule inet filter inbound ip saddr @LANv4 tcp dport 3306 accept
add rule inet filter inbound ip6 saddr @LANv6 tcp dport 3306 accept

# postgres
add rule inet filter inbound ip saddr @LANv4 tcp dport 5432 accept
add rule inet filter inbound ip6 saddr @LANv6 tcp dport 5432 accept