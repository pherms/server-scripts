#!/usr/bin/nft -f

# Web
add rule inet firewall input ip @LANv4 tcp dport { 123 } accept
add rule inet firewall input ip @LANv4 udp dport { 53, 67, 68, 123, 161, 953 } accept
add rule inet firewall input ip6 @LANv6 tcp dport { 123 } accept
add rule inet firewall input ip6 @LANv6 udp dport { 53, 67, 68, 123, 161, 953 } accept