#!/usr/sbin/nft -f

# Web
add rule inet firewall inbound ip saddr @LANv4 tcp dport { 9200, 5601 } accept
add rule inet firewall inbound ip6 saddr @LANv6 tcp dport { 9200, 5601 } accept
