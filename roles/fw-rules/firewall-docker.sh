#!/usr/sbin/nft -f

# IPv4
add rule inet firewall inbound ip saddr @LANv4 tcp dport 80 accept
add rule inet firewall inbound ip6 saddr @LANv6 tcp dport 80 accept

# IPv6
add rule inet firewall inbound ip saddr @LANv4 tcp dport 443 accept
add rule inet firewall inbound ip6 saddr @LANv6 tcp dport 443 accept