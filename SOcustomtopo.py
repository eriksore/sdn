from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
def customNet():
        net = Mininet()        
        #Adding hosts
        pc0 = self.addHost( 'h1' )
        pc1 = self.addHost( 'h2' )
        pc2 = self.addHost( 'h3' )
        pc3 = self.addHost( 'h4' )
        #Adding switches
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

        net.build()
        net.start()

        CLI( net )
        net.stop()

if __name__ =='__main__'
        setLogLevel('info')
        customNet()


topos = { 'mytopo': ( lambda: MyTopo() ) }
