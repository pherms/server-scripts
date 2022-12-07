#!/usr/bin/nft -f

add rule inet firewall input tcp dport { 80, 443 } accept