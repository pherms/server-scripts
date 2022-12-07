#!/usr/bin/nft -f

# Mysql
add rule inet firewall input ip @LANv4 tcp dport 3306 accept
add rule inet firewall input ip6 @LANv6 tcp dport 3306 accept

# postgres
add rule inet firewall input ip @LANv4 tcp dport 5432 accept
add rule inet firewall input ip6 @LANv6 tcp dport 5432 accept