#!/usr/sbin/nft -f

# Ventrilo
add rule inet firewall input ip @LANv4 { tcp, udp } dport { 3784 } accept
add rule inet firewall input ip6 @LANv6 { tcp, udp } dport { 3784 } accept
