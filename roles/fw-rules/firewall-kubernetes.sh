#!/usr/sbin/nft -f

# IPv4
add rule inet firewall inbound ip saddr @LANv4 tcp dport { 6443, 2379:2380, 10250, 10259, 10257, 30000:32767 } accept

# IPv6
add rule inet firewall inbound ip6 saddr @LANv6 tcp dport { 6443, 2379:2380, 10250, 10259, 10257, 30000:32767 } accept
