#!/usr/sbin/nft -f

# Ventrilo
add rule inet firewall inbound { tcp, udp } dport { 3784 } accept
