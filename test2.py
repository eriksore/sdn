#!/usr/bin/python
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
	c0 = net.addController( 'c0', ip='127.0.0.1', port=6633)
	
	print "*** Adding switches ***"
	switches = [ net.addSwitch( 's%s' % s ) for s in irange( 1, 6 ) ]
	print switches
	print "*** Adding hosts ***"
	h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
	h2 = net.addHost( 'h2', mac='00:00:00:00:00:02', ip='10.0.0.2/8' )
	h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='10.0.0.3/8' )
	h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.4/8' )
	h5 = net.addHost( 'h5', mac='00:00:00:00:00:05', ip='10.0.0.5/8' )
	h6 = net.addHost( 'h6', mac='00:00:00:00:00:06', ip='10.0.0.6/8' )
	h7 = net.addHost( 'h7', mac='00:00:00:00:00:07', ip='10.0.0.7/8' )
	h8 = net.addHost( 'h8', mac='00:00:00:00:00:08', ip='10.0.0.8/8' )
	
	linkoptscore = dict(bw=1000, delay='0ms', loss=0)
	linkoptsaccess = dict(bw=100, delay='0ms', loss=0)
	linkoptshost = dict(bw=10, delay='0ms', loss=0)
	
	print "*** Add links between switches ***"
	net.addLink(switches[0],switches[1], **linkoptsaccess)
	net.addLink(switches[0],switches[2], **linkoptsaccess)
	net.addLink(switches[0],switches[3], **linkoptscore)
	net.addLink(switches[3],switches[4], **linkoptsaccess)
	net.addLink(switches[3],switches[5], **linkoptsaccess)
	
	print "*** Add links to hosts ***"
	net.addLink(switches[1],h1,**linkoptshost)
	net.addLink(switches[1],h2,**linkoptshost)
	net.addLink(switches[2],h3,**linkoptshost)
	net.addLink(switches[2],h4,**linkoptshost)
	net.addLink(switches[4],h5,**linkoptshost)
	net.addLink(switches[4],h6,**linkoptshost)
	net.addLink(switches[5],h7,**linkoptshost)
	net.addLink(switches[5],h8,**linkoptshost)

	net.build()
	net.start()	
	CLI( net ) 
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	federatedNet()
