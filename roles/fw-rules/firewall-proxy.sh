#!/usr/sbin/nft -f

add rule inet firewall inbound tcp dport { 80, 443 } accept