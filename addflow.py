import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

# If I want to create node objects, but may not need to
class Node(object):
  def __init__(self, nodeId, nodeType):
    self.nodeId = nodeId
    self.nodeType = nodeType

def node_decoder(obj):
  if obj['__type__'] == 'Node':
    return Node(obj['@id'], obj['@type'])
  return obj

baseUrl = 'http://192.168.231.246:8080/controller/nb/v2'
containerName = 'default'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def build_url(baseUrl, service, containerName):
  postUrl = '/'.join([baseUrl, service, containerName])
  return postUrl

resp, content = h.request(build_url(baseUrl, 'topology', containerName), "GET")
print content
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']
print "###"
print odlEdges

resp, content = h.request(build_url(baseUrl, 'switch', containerName) + '/nodes/', "GET")
print "###"
print content

