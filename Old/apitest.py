import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

baseUrl = 'http://192.168.231.246:8080/controller/nb/v2/'
containerName = 'default/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

# Get all the edges/links
resp, topology = h.request(baseUrl + 'topology/' + containerName, "GET")
edgeProperties = json.loads(topology)
odlEdges = edgeProperties['edgeProperties']
print '#### All edges ####'
print json.dumps(odlEdges, indent = 2)

resp, nodes = h.request(baseUrl + 'connectionmanager/nodes/', "GET")
nodeList = json.loads(nodes)
print '#### All nodes ####'
print json.dumps(nodeList, indent = 2)

resp, nodes = h.request(baseUrl + 'hosttracker/default/hosts/active', "GET")
hostList = json.loads(nodes)
print '#### All hosts ####'
print json.dumps(hostList, indent = 2)