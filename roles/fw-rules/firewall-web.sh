#!/usr/sbin/nft -f

# Web
add rule inet firewall inbound tcp dport { 8080 } accept
