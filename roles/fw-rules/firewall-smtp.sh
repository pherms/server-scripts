#!/usr/sbin/nft -f
# add rule inet filter input ip saddr @LANv4 tcp dport 3306 accept
# Samba filesharing
add rule inet firewall inbound ip saddr @LANv4 tcp dport { 25 } accept
add rule inet firewall inbound ip6 saddr @LANv6 tcp dport { 25 } accept
