#!/usr/sbin/nft -f

# Web
add rule inet firewall input tcp dport { 80, 443 } accept
