#!/usr/sbin/nft -f
#add rule inet filter input ip saddr @LANv4 tcp dport 3306 accept
# IPv4
add rule inet filter inbound ip saddr @LANv4 tcp dport { 123 } accept
add rule inet filter inbound ip saddr @LANv4 udp dport { 53, 67, 68, 123, 161, 953 } accept

# IPv6
add rule inet filter inbound ip6 saddr @LANv6 tcp dport { 123 } accept
add rule inet filter inbound ip6 saddr @LANv6 udp dport { 53, 67, 68, 123, 161, 953 } accept