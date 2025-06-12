# DataTransferRate
An api that when hit it will return the data transfer rate using iperf3 in multihop scenario inlcuding 4 raspberry pi and more (to be continued)

Examining the scenario where we wont run olsr, so the routing tables won't be populated, we need to put fixed ips on the routing tables, wo we can measure data transfer rate by running iperf3 client/server. The keyword here is the multihop 

So if a node is reachable from another node e.g. 192.168.2.10 ( iperf client) to 192.168.2.30 (iperf server) then iperf sends tcp packets and eventually the iperf client gets the measurements. But when we need multihop scenario we need to send from 192.168.2.10 to 192.168.2.30 via another node (or nodes) e.g. 192.168.2.20 (or 192.168.2.20 and 192.168.2.40). These nodes act as forwarders and they need to know where to send the packets to, so they need to check on routing tables

