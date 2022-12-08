#!/usr/sbin/nft -f
# add rule inet filter input ip saddr @LANv4 tcp dport 3306 accept
# Samba filesharing
add rule inet filter inbound ip saddr @LANv4 tcp dport { 137, 138, 139, 445 } accept
add rule inet filter inbound ip6 saddr @LANv6 tcp dport { 137, 138, 139, 445 } accept
