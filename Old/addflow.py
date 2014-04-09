import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

baseUrl = 'http://192.168.231.246:8080/controller/nb/v2'
containerName = 'default'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def find_edge(edges, headNode, tailNode):
  for edge in odlEdges:
    if edge['edge']['headNodeConnector']['node']['id'] == headNode and edge['edge']['tailNodeConnector']['node']['id'] == tailNode:
      return edge
  return None
  
def find_ports(edges, headNode, tailNode):
    for edge in odlEdges:
        if edge['edge']['headNodeConnector']['node']['id'] == headNode and edge['edge']['tailNodeConnector']['node']['id'] == tailNode:
            portId = edge['properties']['name']['value']
            return portId
    return None


def put_path(path, odlEdges, srcIP, dstIP, baseUrl):
  for i, node in enumerate(path[1:-1]):
    flowName = "fromIP" + srcIP[-1:] + "Po" + str(i)
    ingressEdge = find_edge(odlEdges, shortest_path[i], node)
    egressEdge = find_edge(odlEdges, node, shortest_path[i+2])
    newFlow = build_flow_entry(flowName, ingressEdge, egressEdge, node, srcIP, dstIP)
    switchType = newFlow['node']['type']
    putUrl = build_flow_url(baseUrl, 'default', switchType, node, flowName)
    # PUT the flow to the controller
    resp, content = put_dict(h, putUrl, newFlow)

def build_flow_entry(flowName, ingressEdge, egressEdge, node, srcIP, dstIP):
  defaultPriority = "500"
  newFlow = {"installInHw":"false"}
  ingressPort = ingressEdge['edge']['tailNodeConnector']['id']
  egressPort = egressEdge['edge']['headNodeConnector']['id']
  switchType = egressEdge['edge']['headNodeConnector']['node']['type']
  newFlow.update({"name":flowName})
  newFlow.update({"node":ingressEdge['edge']['tailNodeConnector']['node']})
  newFlow.update({"ingressPort":ingressPort, "priority":defaultPriority})
  newFlow.update({"actions":"OUTPUT=" + egressPort})
  return newFlow
  

#Second level URL build
def build_url(baseUrl, service, containerName):
  putUrl = '/'.join([baseUrl, service, containerName])
  return putUrl
  
#Build URL to work with flows on nodes
def build_flow_url(baseUrl, containerName, switchType, switchId, flowName):
  putUrl = build_url(baseUrl, 'flowprogrammer', containerName) +'/node'+ '/'.join(['', switchType, switchId,'staticFlow', flowName])
  return putUrl

def put_dict(h, url, d):
  resp, content = h.request(
      uri = url,
      method = 'PUT',
      headers={'Content-Type' : 'application/json'},
      body=json.dumps(d),
      )
  return resp, content
  
def build_flow_rule_for_node():
    return None
    

# Get all the edges/links
resp, content = h.request(build_url(baseUrl, 'topology', containerName), "GET")
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']
#print json.dumps(odlEdges, indent = 2)
# Get all the nodes/switches
resp, content = h.request(build_url(baseUrl, 'switchmanager', containerName) + '/nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']
#print json.dumps(odlNodes, indent = 2)
#Print information about one specific node
resp, content = h.request(build_url(baseUrl, 'switchmanager',containerName) + '/node/OF/00:00:00:00:00:00:00:03', "GET")
nodeParam = json.loads(content)
nodeParameters = nodeParam['nodeConnectorProperties']
#print json.dumps(nodeParameters, indent = 2)

# Put nodes and edges into a graph
graph = nx.Graph()
for node in odlNodes:
  graph.add_node(node['node']['id'])
for edge in odlEdges:
  e = (edge['edge']['headNodeConnector']['node']['id'], edge['edge']['tailNodeConnector']['node']['id'])
  graph.add_edge(*e)
#print "graph.edges()"
print graph.edges()
# Print out graph info as a sanity check
#print "shortest path from 3 to 7" 
shortest_path = nx.shortest_path(graph, "00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:07")
#print shortest_path
srcIP = "10.0.0.1" #raw_input('What is the source IP?> ')
dstIP = "10.0.0.8" #raw_input('What is the destination IP?> ')

put_path(shortest_path, odlEdges, srcIP, dstIP, baseUrl)
put_path(shortest_path, odlEdges, dstIP, srcIP, baseUrl)
#print h.request(build_url(baseUrl, 'topology', containerName), "GET")

#Test to GET out the flows from a node
resp, content = h.request(build_url(baseUrl, 'flowprogrammer', containerName) + '/node/OF/00:00:00:00:00:00:00:03', "GET")
flowConfig = json.loads(content)
flowConf = flowConfig['flowConfig']
#print json.dumps(flowConf, indent = 2)

#Print out the topology
resp, content = h.request(build_url(baseUrl,'topology',containerName),"GET")
allTopology = json.loads(content)
allTopo = allTopology['edgeProperties']
#print json.dumps(allTopo, indent = 2)

#headNode = "00:00:00:00:00:00:00:03"
#tailNode = "00:00:00:00:00:00:00:02"



def add_sp_flows(shortest_path):
    for i in range(len(shortest_path)-1):
        headNode = shortest_path[i]
        tailNode = shortest_path[i+1]
        #Forward flow
        flowName = headNode[21:23] + 'to' + tailNode[21:23] + 'IPto' + dstIP   
        outPutPort = find_ports(edge, shortest_path[i], shortest_path[i+1])
        flowRule = {"node":{"type":"OF", "id":headNode},"installInHw":"true","name":flowName,"etherType":"0x800", "actions":["OUTPUT="+outPutPort[-1]],"priority":"500","nwDst":dstIP}
        putUrl = build_flow_url(baseUrl, 'default',"OF", headNode, flowName)
        resp, content = put_dict(h, putUrl, flowRule)
        #Backward flow
        flowName = tailNode[21:23] + 'to' + headNode[21:23] + 'IPto' + srcIP
        outPutPort = find_ports(edge, shortest_path[i+1], shortest_path[i])
        flowRule = {"node":{"type":"OF", "id":tailNode},"installInHw":"true","name":flowName,"etherType":"0x800", "actions":["OUTPUT="+outPutPort[-1]],"priority":"500","nwDst":srcIP}
        putUrl = build_flow_url(baseUrl, 'default',"OF", tailNode, flowName)
        resp, content = put_dict(h, putUrl, flowRule)
        print flowRule
    print "Flows have been added!"

add_sp_flows(shortest_path)
          











