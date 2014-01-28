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
	c0 = net.addController( 'c0', ip='127.0.0.1', port=6633)
	
	print "*** Adding switches ***"
	switches = [ net.addSwitch( 's%s' % s ) for s in irange( 1, 6 ) ]
	print switches
	print "*** Adding hosts ***"
	hosts = {}
	for h in irange( 1, 4):
		globals()['h'+str(h)] = net.addHost( 'h%s' % h, mac='00:00:00:00:00:0%s' % h, ip='10.0.0.%s/8' % h )
	for h in irange( 5, 8):
		globals()['h'+str(h)] = net.addHost( 'h%s' % h, mac='00:00:00:00:00:0%s' % h, ip='11.0.0.%s/8' % h )
	
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
	print "*** Set all switches to fail-mode STANDALONE"
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s1", "standalone"])
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s2", "standalone"])
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s3", "standalone"])
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s4", "standalone"])
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s5", "standalone"])
	call(["sudo", "ovs-vsctl", "set-fail-mode", "s6", "standalone"])

	CLI( net ) 
	net.stop()
	


if __name__ == '__main__':
	setLogLevel( 'info' )
	federatedNet()
