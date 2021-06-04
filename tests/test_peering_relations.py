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

import json
import ipaddr
import requests
import yaml
import sys

netixlan = 'https://peeringdb.com/api/netixlan'
pdb_data = json.loads(requests.get(url=netixlan).text)
pdb = {}
for connection in pdb_data['data']:
    asn = connection['asn']
    v4 = connection['ipaddr4']
    v6 = connection['ipaddr6']
    if not asn in pdb:
        pdb[asn] = []
    if v4:
        pdb[asn].append(v4)
    if v6:
        pdb[asn].append(v6)

peering_flat = open('peers.yaml').read()

try:
    peerings = yaml.safe_load(peering_flat)
except:
    print("ERROR: the peers.yaml file could not be parsed... please check \
your syntax")
    sys.exit(2)

# IXPs coloclue is connected to

connected_ixps = {
    "amsix": [ipaddr.IPNetwork('80.249.208.0/21'),
              ipaddr.IPNetwork('2001:7f8:1::/64')],
    "nlix": [ipaddr.IPNetwork('193.239.116.0/22'),
             ipaddr.IPNetwork('2001:7f8:13:0:0:0:0:0/64')],
    "asteroid": [ipaddr.IPNetwork('185.1.94.0/24'),
             ipaddr.IPNetwork('2001:7f8:b6:0:0:0:0:0/64')],
    "speedix": [ipaddr.IPNetwork('185.1.95.0/24'),
                ipaddr.IPNetwork('2001:7f8:b7:0:0:0:0:0/64')],
    "frysix": [ipaddr.IPNetwork('185.1.203.0/24'),
                ipaddr.IPNetwork('2001:7f8:10f::205b:0/64')],
    "private-eun": [ipaddr.IPNetwork('62.115.144.32/31'),
                    ipaddr.IPNetwork('2001:2000:3080:0EBC::/126')],
    "multihop-eun": [ipaddr.IPNetwork('4.68.4.43/32'),
                     ipaddr.IPNetwork('2001:1900::4:35/128')]
}

problem = False
found = 0

for asn in peerings:
    as_number = int(asn[2:])

    if 'ignore_peeringdb' not in peerings[asn]:
        peerings[asn]['ignore_peeringdb'] = False

    for keyword in ['export', 'import', 'description']:
        if keyword not in peerings[asn]:
            print("ERROR: missing %s statement in stanza %s" % (keyword, asn))
            sys.exit(2)

    if 'gtsm' in peerings[asn]:
        if not peerings[asn]['gtsm'] in [True, False]:
            print("ERROR: gtsm value can be either 'yes' or 'no' - default is 'no'")
            print(peerings[asn])
            sys.exit(2)

    if 'multihop' in peerings[asn]:
        if not peerings[asn]['multihop'] in [True, False]:
            print("ERROR: multihop value can be either 'yes' or 'no' - default is 'no'")
            print(peerings[asn])
            sys.exit(2)

    for limit in ["ipv4_limit", "ipv6_limit"]:
        if limit in peerings[asn]:
            try:
                l = int(peerings[asn][limit])
            except ValueError:
                print("ERROR: %s must be a positive integer" % limit)
                print(peerings[asn])
                sys.exit(2)
            if not l >= 0:
                print("ERROR: %s must be larger then or equal to 0" % limit)
                print(peerings[asn])
                sys.exit(2)

    # check whether the manually configured peerings are
    # valid IP addresses
    for keyword in ['only_with', 'private_peering']:
        if keyword in peerings[asn]:
            for peer in peerings[asn][keyword]:
                try:
                    peer_ip = ipaddr.IPAddress(peer)
                except ValueError:
                    print("ERROR: %s in %s is not a valid IP" % (peer, asn))
                    sys.exit(2)

    acceptable_exports = ['AS8283:AS-COLOCLUE', 'NOT ANY', 'ANY']
    if not peerings[asn]['export'] in acceptable_exports:
        print("ERROR: export must be one of the following: %s" \
            % " ".join(acceptable_exports))
        problem += 1


    # loop over all our peering partners as described in the yaml
    if as_number not in pdb:
        if peerings[asn]['ignore_peeringdb']:
            continue
        print("ERROR: %s does not have a PeeringDB record" % asn)
        problem += 1
        continue

    anything = 0
    for session in pdb[as_number]:
        # search if we can reach the peer
        for ixp in connected_ixps:
            for subnet in connected_ixps[ixp]:
                if ipaddr.IPAddress(session) in subnet:
                    print("OK: found %s %s on %s" % (asn, session, ixp))
                    anything += 1
                    found += 1
    if not anything and not peerings[asn]['ignore_peeringdb']:
        print("ERROR: no common IXP with %s" % asn)
        problem += 1

if found < 50:
    print("ERROR: too few peers, aborting")
    problem += 1

if problem:
    print("ERROR: detected %s problems" % problem)
    sys.exit(2)

print("HOORAY: All is good, thanks for peering!")
