#!/usr/bin/python
from subprocess import call
from mininet.topo import Topo 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.util import irange



def federatedNet():
	net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

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
	net.addLink(switches[0],switches[1])
	net.addLink(switches[0],switches[2])
	net.addLink(switches[2],switches[4])
	net.addLink(switches[2],switches[3])
	net.addLink(switches[3],switches[4])
	print "*** Add links to hosts ***"
	net.addLink(switches[0],h1)
	net.addLink(switches[4],h2)

	net.build()
	net.start()	
	

	CLI( net ) 
	net.stop()
	


if __name__ == '__main__':
	setLogLevel( 'info' )
	federatedNet()
