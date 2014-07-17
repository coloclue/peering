#!/usr/bin/env python

import ipaddr
import yaml
import sys

peering_flat = open('peers.yaml').read()

peerings = yaml.safe_load(peering_flat)

# IXPs coloclue is connected to

connected_ixps = {
    "amsix": [ipaddr.IPNetwork('195.69.144.0/22'),
              ipaddr.IPNetwork('2001:7f8:1::/64')]}

for asn in peerings:
    for peer in peerings[asn]['peerings']:
        try:
            peer_ip = ipaddr.IPAddress(peer)
        except ValueError:
            print "ERROR: %s in %s is not a valid IP" % (peer, asn)
            sys.exit(2)

        # search if we can reach the peer
        found = False
        for ixp in connected_ixps:
            for subnet in connected_ixps[ixp]:
                if ipaddr.IPAddress(peer) in subnet:
                    print "OK: found %s in %s" % (peer, ixp)
                    found = True
        if not found:
            print "ERROR: AS 8283 cannot reach %s through %s, either a typo \
or we are not connected to the same internet exchange" \
                % (peer, " ".join(connected_ixps))
            sys.exit(2)

    if not peerings[asn]['export'] in ['AS-COLOCLUE', 'NOT ANY', 'none']:
        print "ERROR: export must be one of the following: %s" \
            % " ".join(['AS-COLOCLUE', 'NOT ANY', 'none'])
        sys.exit(2)
