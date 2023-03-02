#!/usr/sbin/nft -f

add rule inet firewall inbound tcp dport { 443 } accept