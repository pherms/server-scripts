#!/usr/bin/nft -f

# Samba filesharing
add rule inet firewall inbound ip @LANv4 tcp dport { 25 } accept
add rule inet firewall inbound ip6 @LANv6 tcp dport { 25 } accept
