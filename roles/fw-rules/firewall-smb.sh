#!/usr/bin/nft -f

# Samba filesharing
add rule inet firewall inbound ip @LANv4 tcp dport { 137, 138, 139, 445 } accept
add rule inet firewall inbound ip6 @LANv6 tcp dport { 137, 138, 139, 445 } accept
