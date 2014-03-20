import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

baseUrl = 'http://192.168.231.246:8080/controller/nb/v2'
containerName = 'default'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def put_dict(h, url, d):
  resp, content = h.request(
      uri = url,
      method = 'PUT',
      headers={'Content-Type' : 'application/json'},
      body=json.dumps(d),
      )
  return resp, content
  
def build_flow_url(baseUrl, containerName, switchType, switchId, flowName):
  putUrl = build_url(baseUrl, 'flowprogrammer', containerName) +'/node'+ '/'.join(['', switchType, switchId,'staticFlow', flowName])
  return putUrl
  
def build_url(baseUrl, service, containerName):
  putUrl = '/'.join([baseUrl, service, containerName])
  return putUrl
  
def find_ports(edges, headNode, tailNode):
    for edge in get_edges():
        if edge['edge']['headNodeConnector']['node']['id'] == headNode and edge['edge']['tailNodeConnector']['node']['id'] == tailNode:
            portId = edge['properties']['name']['value']
            return portId
    return None  

def build_flow_rule(flowName, node, dstIP, output):
    flowRule = {"node":{"type":"OF", "id":node}}
    flowRule.update({"installInHw":"False"})
    flowRule.update({"name":flowName})
    flowRule.update({"ethertype":"0x800"})
    flowRule.update({"actions":["OUTPUT="+output]})
    flowRule.update({"priority":"500"})
    flowRule.update({"nwDst":dstIP})
    return flowRule

def get_edges():
    resp, content = h.request(build_url(baseUrl, 'topology', containerName),"GET")
    edgeProperties = json.loads(content)
    edges = edgeProperties['edgeProperties']
    return edges
def get_nodes():
    resp, content = h.request(build_url(baseUrl, 'switchmanager', containerName) + '/nodes/', "GET")
    nodeProperties = json.loads(content)
    nodes = nodeProperties['nodeProperties']
    return nodes
def get_sp(edges, nodes, src, dst):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node['node']['id'])
    for edge in edges:
        e = (edge['edge']['headNodeConnector']['node']['id'], edge['edge']['tailNodeConnector']['node']['id'])
        graph.add_edge(*e)
    sp = nx.shortest_path(graph, src, dst)
    return sp

def get_node_specific(id):
    resp, content = h.request(build_url(baseUrl, 'switchmanager', containerName) + '/node/OF/' + id, "GET")
    nodeProperties = json.loads(content)
    nodes = nodeProperties['nodeConnectorProperties']
    return nodes

def get_active_hosts():
    resp, content = h.request(build_url(baseUrl, 'hosttracker', containerName) + '/hosts/active/', "GET")
    hostConfig = json.loads(content)
    hosts = hostConfig['hostConfig']
    #print json.dumps(hosts, indent = 2)
    return hosts

def host_switch(hosts, IP):
    for host in hosts:
        if host['networkAddress'] == IP:
            switch = host['nodeId']
    return switch


def add_sp_flows(shortest_path):
    for i in range(len(shortest_path)-1):
        headNode = shortest_path[i]
        tailNode = shortest_path[i+1]
        
        #Forward flow
        flowName = headNode[21:23] + 'to' + tailNode[21:23] + 'IPto' + dstIP   
        outPutPort = find_ports(get_edges(), shortest_path[i], shortest_path[i+1])
        outPutPortShort = outPutPort[-1]
        putUrl = build_flow_url(baseUrl, 'default',"OF", headNode, flowName)
        resp, content = put_dict(h, putUrl, build_flow_rule(flowName, headNode, dstIP, outPutPortShort))
        
        #Backward flow
        flowName = tailNode[21:23] + 'to' + headNode[21:23] + 'IPto' + srcIP
        outPutPort = find_ports(get_edges(), shortest_path[i+1], shortest_path[i])
        putUrl = build_flow_url(baseUrl, 'default',"OF", tailNode, flowName)
        resp, content = put_dict(h, putUrl, build_flow_rule(flowName, tailNode, srcIP, outPutPortShort))
    print "Flows have been added!"
    
    
srcIP = raw_input('What is the source IP?> ')
dstIP = raw_input('What is the destination IP?> ')
hosts = get_active_hosts()
print "\nThe host with IP " + srcIP + " is connected to switch: " + host_switch(hosts, srcIP)
print "The host with IP " + dstIP + " is connected to switch: " + host_switch(hosts, dstIP)
shortest_path = get_sp(get_edges(), get_nodes(), host_switch(hosts, srcIP), host_switch(hosts, dstIP))
print "\nThe shortest path between these nodes are: " 
print shortest_path
add_sp_flows(shortest_path)




