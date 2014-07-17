Coloclue (AS8283) Peering Relation Repository
==============================================

## What is Coloclue? ##

Coloclue (AS 8283) is a non-profit foundation based in the Netherlands, serving
a very specific market segment: the foundation is run by, and for, network
engineers from the Dutch ISP scene, entirely driven by volunteers.

These engineers prefer to host their gear at some other place than their
employer. This benefits them hugely in troubleshooting and provides for a
neutral environment.

## How to peer? ##

If you are connected to AMS-IX you can set up BGP sessions with AS 8283. Make
sure you accept `AS-COLOCLUE` (50 prefixes max).

Add yourself to the peers.yaml file and submit a pull request to this
repository. Once a network engineer validates your pull request and merges it
into the master branch, the peering session will automatically be configured on
our routers within an hour or so.

The peers.yaml format should be fairly self-explanatory, but when in doubt do
not hesitate to contact routers@coloclue.net.

### Technical details ###

```
    Name:  Netwerkvereniging Coloclue
    ASN:   AS8283
    Macro: AS-COLOCLUE
    NOC:   routers@coloclue.net

    IXP:   AMS-IX
    IPv4:  195.69.147.161
    IPv6:  2001:7f8:1::a500:8283:1
```

## Routing Policy ##

Coloclue (AS8283) has a fairly open peering policy, but we do have a
non-traditional routing policy:
    
    * All peers' prefixes are filtered based on strict RPSL
    * Same local preference for peers/downstream/upstream
    * Prefix filters facing peers are updated every 12 hours from RADB

