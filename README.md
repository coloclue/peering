Coloclue (AS8283) Peering Relation Repository
==============================================

What is Coloclue?
-------------------

How to peer?
------------

If you are connected to AMS-IX you can set up BGP sessions with AS 8283. Make
sure you accept AS-COLOCLUE (50 prefixes max).

Add yourself to the peers.yaml file and submit a pull request to this
repository. Once a network engineer validates your pull request and merges it
into the master branch, the peering session will automatically be configured on
our routers within an hour or so.

The peers.yaml format should be fairly self-explanatory, but when in doubt do
not hesitate to contact routers@coloclue.net.

Routing Policy
--------------

Coloclue (AS8283) has a fairly open peering policy, but we do have a
non-traditional routing policy:
    
    * All peers' prefixes are filtered based on strict RPSL
    * Same local preference for peers/downstream/upstream

