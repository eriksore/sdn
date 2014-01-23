
from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import irange

import sys
flush = sys.stdout.flush

class FederatedNet( Topo ):
    "Topology for a federated network."

    def __init__( self, N,  **params ):
    
    	Topo.__init__( self,  **params )
    	
    	hosts1 = [ self.addHost( 'h%d' % n ) 
    			for n in irange( 1, 2 ) ]
	hosts2 = [ self.addHost( 'h%d' % n ) 
    			for n in irange( 3, 4 ) ]
    	hosts3 = [ self.addHost( 'h%d' % n ) 
    			for n in irange( 5, 6 ) ]
    	hosts4 = [ self.addHost( 'h%d' % n ) 
    			for n in irange( 7, 8 ) ]
	switches = [ self.addSwitch( 's%s' % s ) 
			for s in irange( 1, 6 ) ]
		
	for h in hosts1:
		self.addLink( s2, h )
	for h in hosts2:
		self.addLink( s3, h )
	for h in hosts3:
		self.addLink( s5, h )
	for h in hosts4:
		net.addLink( s6, h )
	self.addLink( s1, s2 )
	self.addLink( s1, s4 )
	self.addLink( s1, s3 )
	self.addLink( s4, s5 )
	self.addLink( s4, s6 )

    
if __name__ == '__main__':
	lg.setLogLevel( 'info' )
	hostCount = 8
	FederatedNet( hostCount )
