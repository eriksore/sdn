from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        pc0 = self.addHost( 'h1' )
        pc1 = self.addHost( 'h2' )
        pc2 = self.addHost( 'h3' )
        pc3 = self.addHost( 'h4' )
        switch0 = self.addSwitch( 's1' )
        switch1 = self.addSwitch( 's2' )
        router2 = self.addSwitch( 'r2' )
        router3 = self.addSwitch( 'r3' )
        # Add links
        self.addLink( pc0, switch0 )
        self.addLink( pc1, switch0 )
        self.addLink( pc2, switch1 )
        self.addLink( pc3, switch1 )
        self.addLink( switch0, router3 )
        self.addLink( switch1, router2 )
        self.addLink( router2, router3 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
