#!/usr/sbin/nft -f
flush ruleset                                                                    

table inet firewall {
    # add set inet firewall LANv4 { type ipv4_addr\; flags interval\; }
    # add set inet firewall LANv6 { type ipv6_addr\; flags interval\; }
    # add element inet firewall LANv4 { 192.168.2.0/24 }
    # add element inet firewall LANv6 { 2a02:a462:72b3:1::/64, fe80::5604:a6ff:fe48:9010/64 }

    set LANv4 {
        type ipv4_addr
        flags interval
        elements = { 192.168.2.0/24 }
    }
    set LANv6 {
        type ipv6_addr
        flags interval
        elements = { 2a02:a462:72b3:1::/64, fe80::5604:a6ff:fe48:9010/64 }
    }
    chain inbound_ipv4 {
        # accepting ping (icmp-echo-request) for diagnostic purposes.
        # However, it also lets probes discover this host is alive.
        # This sample accepts them within a certain rate limit:
        #
        icmp type echo-request limit rate 5/second accept      
    }

    chain inbound_ipv6 {                                                         
        # accept neighbour discovery otherwise connectivity breaks
        #
        icmpv6 type { nd-neighbor-solicit, nd-router-advert, nd-neighbor-advert } accept
                                                                                 
        # accepting ping (icmpv6-echo-request) for diagnostic purposes.
        # However, it also lets probes discover this host is alive.
        # This sample accepts them within a certain rate limit:
        #
        icmpv6 type echo-request limit rate 5/second accept
    }

    chain inbound {                                                              

        # By default, drop all traffic unless it meets a filter
        # criteria specified by the rules that follow below.
        type filter hook input priority 0; policy drop;

        # Allow traffic from established and related packets, drop invalid
        ct state vmap { established: accept, related: accept, invalid: drop } 

        # Allow loopback traffic.
        iifname lo accept

        # Jump to chain according to layer 3 protocol using a verdict map
        meta protocol vmap { ip: jump inbound_ipv4, ip6: jump inbound_ipv6 }

        tcp dport { 22 } accept

        iif != lo ip daddr 127.0.0.1/8 counter drop comment "drop connections to loopback not coming from loopback"
		iif != lo ip6 daddr ::1/128 counter drop comment "drop connections to loopback not coming from loopback"
        
        # Uncomment to enable logging of denied inbound traffic
        # log prefix "[nftables] Inbound Denied: " counter drop
    }                                                                            
                                                                                 
    chain forward {                                                              
        # Drop everything (assumes this device is not a router)                  
        type filter hook forward priority 0; policy drop;                        
    }                                                                            
                                                                                 
    # no need to define output chain, default policy is accept if undefined.
}