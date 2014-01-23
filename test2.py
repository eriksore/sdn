#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.util import irange

def federatedNet():
	net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

	print "*** Creating Nodes ***"
	
	c0 = net.addController ( 'c0', ip='127.0.0.1' )

	for s in irange( 1, 6 ):
		net.addSwitch( 's%s' % s )
	for h in irange( 1, 8 ):
		net.addHost( 'h%s' % h, mac='00:00:00:00:00:0%s' % h, ip='10.0.0.%s/8' % h )

	net.build()
	net.start()
	c0.start()
	CLI( net ) 
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	federatedNet()
