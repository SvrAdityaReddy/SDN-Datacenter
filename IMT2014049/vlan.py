#!/usr/bin/env python
import sys
from mininet.node import Host,Controller
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.log import error
from mininet.net import Mininet
from functools import partial
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class VLANHost( Host ):
    def config( self, vlan=100, **params ):
        r = super( VLANHost, self ).config( **params )
        intf = self.defaultIntf()
        self.cmd( 'ifconfig %s inet 0' % intf )
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        newName = '%s.%d' % ( intf, vlan )
        intf.name = newName
        self.nameToIntf[ newName ] = intf

        return r

hosts = { 'vlan': VLANHost }


class VLANTOPO( Topo ):
    def build( self, k=2, n=2, vlanBase=100 ):
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        h1 = self.addHost( 'h1', cls=VLANHost, vlan=100, mac='00:00:00:00:00:01' )
        h2 = self.addHost( 'h2', cls=VLANHost, vlan=100, mac='00:00:00:00:00:02' )
        h3 = self.addHost( 'h3', cls=VLANHost, vlan=200, mac='00:00:00:00:00:03' )
        h4 = self.addHost( 'h4', cls=VLANHost, vlan=200, mac='00:00:00:00:00:04' )
        h5 = self.addHost( 'h5', cls=VLANHost, vlan=100, mac='00:00:00:00:00:05' )
        h6 = self.addHost( 'h6', cls=VLANHost, vlan=100, mac='00:00:00:00:00:06' )
        h7 = self.addHost( 'h7', cls=VLANHost, vlan=200, mac='00:00:00:00:00:07' )
        h8 = self.addHost( 'h8', cls=VLANHost, vlan=200, mac='00:00:00:00:00:08' )
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( h3, s1 )
        self.addLink( h4, s1 )
        self.addLink( h5, s2 )
        self.addLink( h6, s2 )
        self.addLink( h7, s2 )
        self.addLink( h8, s2 )
        self.addLink(s1,s2)


if __name__ == '__main__':

    setLogLevel( 'info' )
    c0 = Controller( 'c2')

    net = Mininet( topo=VLANTOPO() )
    net.addController(c0)
    net.start()
    CLI( net )
    net.stop()
