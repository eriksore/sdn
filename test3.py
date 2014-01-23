#!/usr/bin/python

"""
Script created by VND - Visual Network Description
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSLegacyKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology():
    "Create a network."
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )
    s5 = net.addSwitch( 's5' )
    s6 = net.addSwitch( 's6' )
    h12 = net.addHost( 'h12', mac='00:00:00:00:00:12', ip='10.0.0.12/8' )
    #print h12
    h13 = net.addHost( 'h13', mac='00:00:00:00:00:13', ip='10.0.0.13/8' )
    h14 = net.addHost( 'h14', mac='00:00:00:00:00:14', ip='10.0.0.14/8' )
    h15 = net.addHost( 'h15', mac='00:00:00:00:00:15', ip='10.0.0.15/8' )
    h16 = net.addHost( 'h16', mac='00:00:00:00:00:16', ip='10.0.0.16/8' )
    h17 = net.addHost( 'h17', mac='00:00:00:00:00:17', ip='10.0.0.17/8' )
    h18 = net.addHost( 'h18', mac='00:00:00:00:00:18', ip='10.0.0.18/8' )
    h19 = net.addHost( 'h19', mac='00:00:00:00:00:19', ip='10.0.0.19/8' )

    print "*** Creating links"
    net.addLink(s6, h19, 3, 0)
    net.addLink(s6, h18, 2, 0)
    net.addLink(s5, h17, 3, 0)
    net.addLink(s5, h16, 2, 0)
    net.addLink(s3, h15, 3, 0)
    net.addLink(s3, h14, 2, 0)
    net.addLink(s2, h13, 3, 0)
    net.addLink(s2, h12, 2, 0)
    net.addLink(s4, s6, 3, 1)
    net.addLink(s4, s5, 2, 1)
    net.addLink(s1, s3, 3, 1, bw=10, delay='10ms', loss=1)
    net.addLink(s1, s2, 2, 1)
    net.addLink(s1, s4, 1, 1)

    print "*** Starting network"
    net.build()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

