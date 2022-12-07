#!/usr/sbin/nft -f

# Web
add rule inet firewall inbound tcp dport { 80, 443 } accept
