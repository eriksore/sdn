#External libraries
import sys
import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2
from xml.dom import minidom
from lxml import etree
#Own libraries
import restconf
import frontend

#Base URLs for Config and operational
baseUrl = 'http://192.168.231.246:8080'
confUrl = baseUrl + '/restconf/config/' #Contains data inserted via controller
operUrl = baseUrl + '/restconf/operational/' # Contains other data
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
#Specific REST URLs



h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

flowIdCounter = int(100)
hosts = restconf.get_active_hosts()
srcIP = '10.0.0.1'
destIP = '10.0.0.2'
nodes = restconf.get_topology(restconf.get(findTopology))#['topology'][0]['node']
#print nodes
nodes = restconf.get_topology(restconf.get(findTopology))['topology'][0]['node']
"""
for node in nodes:
    print node['node-id']
    tables = restconf.get('http://192.168.231.246:8080/restconf/operational/opendaylight-inventory:nodes/node/'+node['node-id'])
    flowTables = json.loads(tables)
    try:
        for table in flowTables['node'][0]['flow-node-inventory:table']:
            if table['opendaylight-flow-table-statistics:flow-table-statistics']['opendaylight-flow-table-statistics:active-flows'] != 0:
                try:
                    flowRules = restconf.get(confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+str(table['flow-node-inventory:id']))
                    rules = json.loads(flowRules)
                    for rule in rules['flow-node-inventory:table'][0]['flow-node-inventory:flow']:
                        
                        if rule['flow-node-inventory:match']['flow-node-inventory:ipv4-destination'] == srcIP:
                            table = str(table['flow-node-inventory:id'])
                            flowId = str(rule['flow-node-inventory:id'])
                            url = confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+table+'/flow/'+flowId
                            #restconf.delete(url)
                        elif rule['flow-node-inventory:match']['flow-node-inventory:ipv4-destination'] == destIP:
                            table = str(table['flow-node-inventory:id'])
                            flowId = str(rule['flow-node-inventory:id'])
                            url = confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+table+'/flow/'+flowId
                            #restconf.delete(url)
                except ValueError:
                    pass
    except KeyError:
        pass"""
print confUrl+'opendaylight-inventory:nodes/node/openflow:2/table/0'
flowRules2 = restconf.get(confUrl+'opendaylight-inventory:nodes/node/openflow:2/table/0')
flowRules3 = restconf.get(confUrl+'opendaylight-inventory:nodes/node/openflow:3/table/0')
print flowRules2
print flowRules3
