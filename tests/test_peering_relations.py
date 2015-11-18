#!/usr/bin/env python
# test_peering_relations.py
#
# Purpose:
#   Simple peers.yaml parser to do some basic checks this is useful
#   to give immediate feedback to the pull requester when obvious
#   things are wrong.
#
# Author: Job Snijders <job@instituut.net>
# License: BSD 2-Clause

import ipaddr
import yaml
import sys

peering_flat = open('peers.yaml').read()

try:
    peerings = yaml.safe_load(peering_flat)
except:
    print "ERROR: the peers.yaml file could not be parsed... please check \
your syntax"
    sys.exit(2)

# IXPs coloclue is connected to

connected_ixps = {
    "amsix": [ipaddr.IPNetwork('80.249.208.0/21'),
              ipaddr.IPNetwork('2001:7f8:1::/64')],
    "nlix": [ipaddr.IPNetwork('193.239.116.0/23'),
             ipaddr.IPNetwork('2001:7f8:13:0:0:0:0:0/64')],
    "private-eun": [ipaddr.IPNetwork('62.115.144.32/31'),
                    ipaddr.IPNetwork('2001:2000:3080:0EBC::/126')]
}

for asn in peerings:
    for keyword in ['export', 'import', 'description', 'peerings']:
        if keyword not in peerings[asn]:
            print "ERROR: missing %s statement in stanza %s" % (keyword, asn)
            sys.exit(2)

    if 'gtsm' in peerings[asn]:
        if not peerings[asn]['gtsm'] in [True, False]:
            print "ERROR: gtsm value can be either 'yes' or 'no' - default is 'no'"
            print peerings[asn]
            sys.exit(2)

    for limit in ["ipv4_limit", "ipv6_limit"]:
        if limit in peerings[asn]:
            try:
                l = int(peerings[asn][limit])
            except ValueError:
                print "ERROR: %s must be a positive integer" % limit
                print peerings[asn]
                sys.exit(2)
            if not l > 0:
                print "ERROR: %s must be larger then 1" % limit
                print peerings[asn]
                sys.exit(2)

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
                    print "OK: found %s (%s) in %s" % (peer, asn, ixp)
                    found = True
        if not found:
            print "ERROR: AS 8283 cannot reach %s through %s, either a typo \
or we are not connected to the same internet exchange" \
                % (peer, " ".join(connected_ixps))
            sys.exit(2)

    acceptable_exports = ['AS-COLOCLUE', 'NOT ANY', 'ANY']
    if not peerings[asn]['export'] in acceptable_exports:
        print "ERROR: export must be one of the following: %s" \
            % " ".join(acceptable_exports)
        sys.exit(2)

print "HOORAY: All is good, thanks for peering!"
