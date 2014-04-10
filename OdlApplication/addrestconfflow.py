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
"""
try:
  from lxml import etree
  print("running with lxml.etree \n")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+ \n")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+ \n")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree \n")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree \n")
        except ImportError:
          print("Failed to import ElementTree from any known place  \n")
"""
#Base URLs for Config and operational
baseUrl = 'http://192.168.231.246:8080'
confUrl = baseUrl + '/restconf/config/' #Contains data inserted via controller
operUrl = baseUrl + '/restconf/operational/' # Contains other data

#"Old" REST APIs that still are used
sdSalUrl = baseUrl + '/controller/nb/v2/'

#Specific REST URLs
findNodes = operUrl + '/opendaylight-inventory:nodes/'
findTopo = operUrl + '/network-topology:network-topology/'
findNodeConnector = operUrl + '/opendaylight-inventory:nodes/node/node-connector/'
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
findFlow = confUrl +'/opendaylight-inventory:nodes/node/openflow:1/table/0/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def get_nodes(xml):
    pre = json.loads(xml)
    nodes = pre['nodes']['node']
    return nodes

def get_topology(xml):
    topology = json.loads(xml)
    nodes = topology['topology'][0]['node']
    #for node in nodes:
    #    print node['node-id']
    links = topology['topology'][0]['link']
    #for link in links:
    #    print "Source:      "+ link['source']['source-tp']
    #    print "Destination: " + link['destination']['dest-tp']
    #print json.dumps(topology, indent = 2)
    return topology

def get_sp(topology, src, dst):
    graph = nx.Graph()
    nodes = topology['topology'][0]['node']
    links = topology['topology'][0]['link']
    for node in nodes:
        graph.add_node(node['node-id'])
    for link in links:
        e = (link['source']['source-node'], link['destination']['dest-node'])
        graph.add_edge(*e)
    sp = nx.shortest_path(graph, src, dst)
    return sp

def host_switch(hosts, IP):
    for host in hosts:
        if host['networkAddress'] == IP:
            switch = host['nodeId']
    return switch

def find_ports(xml, headNode, tailNode):
    links = xml['topology'][0]['link']
    for link in links:
        if link['source']['source-node'] == headNode and link['destination']['dest-node'] == tailNode:
            portId = link['source']['source-tp']
            return portId
    return None
    
def add_sp_flows(shortest_path):
    for i in range(len(shortest_path)-1):
        headNode = shortest_path[i]
        tailNode = shortest_path[i+1]
        
        #Forward Flow
        flowName = headNode + 'to' + tailNode + 'IPto' + dstIP
        outPutPort = find_ports(get_topology(restconf.get(h, findTopology)), shortest_path[i], shortest_path[i+1])
        print flowName
        print outPutPort
        
        #Backward Flow
        flowName = tailNode + 'to' + headNode + 'IPto' + srcIP
        outPutPort = find_ports(get_topology(restconf.get(h, findTopology)), shortest_path[i+1], shortest_path[i])
        print flowName
        print outPutPort
        
def get_flows(xml):
    flows = json.loads(xml)
    print flows['flow-node-inventory:table'][0]['flow-node-inventory:flow']
    
def build_flow_rule_sp(dstIp):
    flowRule = {} 
    return None

srcIP = '10.0.0.1' #raw_input('What is the source IP?> ')
dstIP = '10.0.0.8' #raw_input('What is the destination IP?> ')
hosts = restconf.get_active_hosts()
#print "\nThe host with IP " + srcIP + " is connected to switch: " + host_switch(hosts, srcIP)
#print "The host with IP " + dstIP + " is connected to switch: " + host_switch(hosts, dstIP)
shortest_path = get_sp(get_topology(restconf.get(findTopology)), host_switch(hosts, srcIP), host_switch(hosts, dstIP))
#print "\nThe shortest path between these nodes are: " 
#print shortest_path
#add_sp_flows(shortest_path)
content = restconf.get('http://192.168.231.246:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/')
#print content
#flows = json.loads(content)
#print json.dumps(flows, indent=2)

ip = '10.0.0.10'
""""for flow in flows['flow-node-inventory:table'][0]['flow-node-inventory:flow']: 
    print flow['flow-node-inventory:id']
    print flow['flow-node-inventory:match']['flow-node-inventory:ipv4-destination']
    print flow['flow-node-inventory:instructions']['flow-node-inventory:instruction'][0]['flow-node-inventory:apply-actions']['flow-node-inventory:action'][0]['flow-node-inventory:output-action']['flow-node-inventory:output-node-connector']
"""

def flow_rule_base(flowName, tableId, flowId, hardTimeout, idleTimeout):
    flow = etree.Element("flow")
    flow.set('xlmns','urn:opendaylight:flow:inventory')
    strict = etree.SubElement(flow, "strict")
    strict.text = "false"
    flow_name = etree.SubElement(flow, "flow-name")
    flow_name.text = flowName
    id = etree.SubElement(flow, "id") #ID of the flow
    id.text = flowId
    table_id = etree.SubElement(flow, "table_id") #ID of the table on that switch
    table_id.text = tableId
    hard_timeout = etree.SubElement(flow, "hard-timeout")
    hard_timeout.text = hardTimeout
    idle_timeout = etree.SubElement(flow, "idle-timeout")
    idle_timeout.text = idleTimeout
    priority = etree.SubElement(flow, "priority")
    priority.text = "2"
    cookie = etree.SubElement(flow, "cookie")
    cookie.text = "1"
    barrier = etree.SubElement(flow, "barrier")
    barrier.text = "false"
    cookie_mask = etree.SubElement(flow, "cookie_mask")
    cookie_mask.text = "255"
    installHw = etree.SubElement(flow, "installHw")
    installHw.text = "True"
    
    #The Actions
    instructions = etree.SubElement(flow, "instructions")
    instruction = etree.SubElement(instructions, "instruction")
    order_instruct = etree.SubElement(instruction, "order")
    order_instruct.text = "0"
    apply_actions = etree.SubElement(instruction, "apply-actions")
    action = etree.SubElement(apply_actions, "action")
    order_action = etree.SubElement(action, "order")
    order_action.text = "0"
    etree.SubElement(action, "flood-all-action")
    
    #The Matches
    match = etree.SubElement(flow, "match")
    ethernet_match = etree.SubElement(match, "ethernet-match")
    ethernet_type = etree.SubElement(ethernet_match, "ethernet-type")
    type = etree.SubElement(ethernet_type, "type")
    type.text = "2048"
    ipv4 = etree.SubElement(match,"ipv4-destination")
    ipv4.text = "11.11.11.11/8"
    return flow

def add_flow_match(flow, matches):
    match = flow.xpath('//match')[0]
    for newmatch in matches:
        etree.SubElement(match, newmatch)
    return None    
        
def add_flow_action(flow, actions):
    action = flow.xpath('//action')[0]
    for newaction in actions:
        etree.SubElement(action, newaction)
    return flow


#print(etree.tostring(flow_rule_base("FooBarXXX","1","127","666","666"), pretty_print=True, xml_declaration=True, encoding="utf-8", standalone=False))
#body = etree.tostring(flow_rule_base("FooBarXXX","1","127","666","666"), xml_declaration=True, encoding="utf-8", standalone=False)
#print restconf.put(h, 'http://192.168.231.246:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:2/table/1/flow/127', etree.tostring(flow_rule_base("FooBarXXX","1","127","666","666"), xml_declaration=True, encoding="utf-8", standalone=False))
action = []
match = []
answer = frontend.main_menu()
if answer == 'addFlow':
    answer = frontend.show_act_mat()
    if answer == 'addFlow':
        _node, _tableId, _flowId, _flowName, _hardTimeOut, _idleTimeOut = frontend.add_flow_gui()
        newFlow = flow_rule_base(_flowName, _tableId, _flowId, _hardTimeOut, _idleTimeOut)
        newFlow = frontend.add_actions(newFlow)
        newFlow = frontend.add_matches(newFlow)
        frontend.main_menu()
    else:
        frontend.main_menu()
elif answer == 'lookFlows':
    print json.dumps(frontend.view_flows(), indent=2)
    print '\n'
    frontend.main_menu()
elif answer == 'delFlow':
    frontend.del_flow()
    frontend.main_menu()
else:
    frontend.main_menu()

        
        
