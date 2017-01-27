#!/usr/bin/env python

import json
import yaml

peering_flat = open('peers.yaml').read()
peerings = yaml.safe_load(peering_flat)

r = json.loads(open('net.json').read())

pdb = {}
for i in r['data']:
    pdb[i['asn']] = i['irr_as_set']

for asn in peerings:
    if 'import' in peerings[asn]:
        asn2 = int(asn.replace('AS', ''))
        if asn2 in pdb:
            local_ver = peerings[asn]['import']
            pdb_ver = pdb[asn2]
            if not pdb_ver:
                continue
            if local_ver != pdb_ver:
                print "local: %s, pdb: %s" % (peerings[asn]['import'], pdb[asn2])
