Coloclue (AS8283) Peering Relation Repository
==============================================

Current Peering Policy: ![peers.yaml status](https://github.com/coloclue/peering/actions/workflows/test_peers.yaml.yml/badge.svg)

## What is Coloclue? ##

Coloclue (AS 8283) is a non-profit association based in the Netherlands, serving
a very specific market segment: the association is run by, and for, network
engineers from the Dutch ISP scene, entirely driven by volunteers.

These engineers prefer to host their gear at some other place than their
employer. This benefits them hugely in troubleshooting and provides for a
neutral environment.

## How to peer? ##

If you are connected to AMS-IX, NL-IX, Asteroid Amsterdam, SPEED-IX, LSIX, FrysIX,
DE-CIX, France-IX or SwissIX you can set up BGP sessions with AS8283. Make sure you
accept `AS8283:AS-COLOCLUE` (100 prefixes max).

Add yourself to the `peers.yaml` file and submit a pull request to this
repository. Once a network engineer validates your pull request and merges it
into the master branch, the peering session will automatically be configured on
our routers within an hour or so.

The `peers.yaml` format should be fairly self-explanatory, but when in doubt do
not hesitate to contact routers@coloclue.net.

**Note**: `peers.yaml` is indented by **4** spaces. This needs to be used
consistently across the file. Failing to do so will result in invalid YAML.

Example stanza:

```
AS12345:
    description: A really cool ISP
    import: AS-RANDOMISP
    export: AS8283:AS-COLOCLUE
```

The relevant IPv4 and IPv6 addresses are pulled from PeeringDB. If you add a
new connection in PeeringDB, and we have an Internet Exchange in common,
our software will automatically set up BGP peering sessions towards your
new connection. Likewise, if you remove an connection from your PeeringDB
record, our software will remove the respective BGP sessions.

### Technical details ###

```
Name:  Netwerkvereniging Coloclue
ASN:   AS8283
Macro: AS8283:AS-COLOCLUE
NOC:   routers@coloclue.net

IXP:   AMS-IX
IPv4:  80.249.211.161
IPv6:  2001:7f8:1::a500:8283:1

IXP:   NL-IX
IPv4:  193.239.117.111
       193.239.117.203
IPv6:  2001:7f8:13::a500:8283:1 
       2001:7f8:13::a500:8283:2

IXP:   Asteroid Amsterdam
IPv4:  185.1.94.15
IPv6:  2001:7f8:b6::205b:1

IXP:   SPEED-IX
IPv4:  185.1.95.16
IPv6:  2001:7f8:b7::a500:8283:1

IXP:   Frys-IX
IPv4:  185.1.203.140
IPv6:  2001:7f8:10f::205b:140

IXP:   DE-CIX (Frankfurt)
IPv4:  80.81.197.51
IPv6:  2001:7f8::205b:0:1

IXP:   France-IX (Paris)
IPv4:  37.49.238.29
IPv6:  2001:7f8:54::2:29

IXP:   SwissIX
IPv4:  91.206.53.24
IPv6:  2001:7f8:24::118
```

## Routing Policy ##

Coloclue (AS8283) has a fairly open peering policy, but we do have a
non-traditional routing policy:

    * If your IXP connection is NOT in PeeringDB, changes will need to be handled manually
    * All peers' prefixes are filtered based on strict IRR.
    * All peers' prefixes are filtered based on strict RPKI.
    * Prefix filters facing peers are updated every 12 hours from `rr.ntt.net`.

We provision our configuration automatically from PeeringDB, please ensure your entry is kept up-to-date including IP addresses and number of prefixes announced.
