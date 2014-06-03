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

for node in nodes:
    print node['node-id']
    tables = restconf.get('http://192.168.231.246:8080/restconf/operational/opendaylight-inventory:nodes/node/'+node['node-id'])
    flowTables = json.loads(tables)
    #print tables
    try:
        for table in flowTables['node'][0]['flow-node-inventory:table']:
            if table['opendaylight-flow-table-statistics:flow-table-statistics']['opendaylight-flow-table-statistics:active-flows'] != 0:
                print table['flow-node-inventory:id']
                #print confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+str(table['flow-node-inventory:id'])
                try:
                    flowRules = restconf.get(confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+str(table['flow-node-inventory:id']))
                    #print confUrl+'opendaylight-inventory:nodes/node/'+node['node-id']+'/table/'+str(table['flow-node-inventory:id'])
                    #flowRules = restconf.get(confUrl+'opendaylight-inventory:nodes/node/openflow:3/table/0')
                    rules = json.loads(flowRules)
                    print rules
                except ValueError:
                    pass
                #print rules['flow-node-inventory:table'][0]['flow-node-inventory:flow']
                #flowRules['flow-node-inventory:table'][0]['flow-node-inventory:flow']
                """try:
                    for rule in flowRules:
                        if rule['flow-node-inventory:match']['flow-node-inventory:ipv4-destination'] == destIP:
                            print "found"
                except KeyError:
                    pass"""
    except KeyError:
        pass
"""
tables = restconf.get('http://192.168.231.246:8080/restconf/operational/opendaylight-inventory:nodes/node/openflow:1')
flowtables = json.loads(tables)
print flowtables['node'][0]['flow-node-inventory:table']
flowRules = restconf.get(confUrl+'opendaylight-inventory:nodes/node/openflow:1/table/0')
rules = json.loads(flowRules)
print rules['flow-node-inventory:table'][0]['flow-node-inventory:flow']                
#print flowRules
"""
"""
            
    #print json.dumps(flows, indent=2)
    
#content = restconf.get('http://192.168.231.246:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0')#node/openflow:1/table/0/')
content = restconf.get('http://192.168.231.246:8080/restconf/operational/opendaylight-inventory:nodes/node/openflow:1')
flows = json.loads(content)
#print flows['flow-node-inventory:table'][0]['flow-node-inventory:flow']

#print json.dumps(flows['flow-node-inventory:table'][0]['flow-node-inventory:flow'], indent=2)
#print json.dumps(flows, indent=2)
"""