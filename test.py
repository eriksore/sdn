from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import irange

def federatedNet():
	net = Mininet( controller=Controller, switch=OVSSwitch, build=False )

	c1 = net.addController ( 'c1', ip='127.0.0.1' )

	for h in irange( 1, 8 ):
		net.addHost( 'h%s' % h )
	for s in irange( 1, 6 ):
		net.addSwitch( 's%s' % s )
	


	net.build()
	net.start()
	c1.start()
	CLI( net )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	federatedNet()

