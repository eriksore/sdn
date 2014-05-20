from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import irange

import sys
flush = sys.stdout.flush

net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch, protocols=OpenFlow13)

print "*** Creating Nodes ***"
print "*** Adding remote controller ***"
c0 = net.addController( 'c0', ip='192.168.231.246', port=6633)
print "*** Adding switches ***"
switches = [ net.addSwitch( 's%s' % s ) for s in irange( 1, 5 ) ]
print switches
print "*** Adding hosts ***"
hosts = {}
for h in irange( 1, 2):
    globals()['h'+str(h)] = net.addHost( 'h%s' % h, mac='00:00:00:00:00:0%s' % h, ip='10.0.0.%s/8' % h )
print "*** Add links between switches ***"
net.addLink(s1,s2)
net.addLink(s1,s3)
net.addLink(s2,s5)
net.addLink(s3,s4)
net.addLink(s4,s5)
print "*** Add links to hosts ***"
net.addLink(s1,h1)
net.addLink(s5,h2)

net.build()
net.start()
CLI( net )
net.stop