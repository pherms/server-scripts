#!/usr/sbin/nft -f

# Web
add rule inet firewall inbound tcp dport { 9200, 5601 } accept
