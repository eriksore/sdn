import sys
import json
import httplib2

#Base URLs for Config and operational
baseUrl = 'http://192.168.231.255:8080'
confUrl = baseUrl + '/restconf/config'
operUrl = baseUrl + '/restconf/operational'

#"Old" REST APIs that still are used
sdSalUrl = baseUrl + '/controller/nb/v2/'

#Specific REST URLs
findNodes = operUrl + '/opendaylight-inventory:nodes/'
findTopo = operUrl + '/network-topology:network-topology/'
findNodeConnector = operUrl + '/opendaylight-inventory:nodes/node/node-connector/'
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
findFlow = confUrl +'/opendaylight-inventory:nodes/node/openflow:1/table/0/'
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

#GET function. Retrieve information  
def get(url):
    resp, xml = h.request(
        url,
        method = "GET",
        headers = {'Content-Type' : 'application/xml'}
        )
    return xml
#Put function. 
def put(url, body):
    resp, content = h.request(
        url, 
        method = "PUT",
        body = body,
        headers = {'Content-Type' : 'application/xml', 'Accept':'application/xml'}
        )
    return resp, content
#DELETE function
def delete(url):
    resp, content = h.request(
        url,
        method = "DELETE"
        )
    return resp
#Find active hosts    
def get_active_hosts():
    resp, content = h.request(sdSalUrl + 'hosttracker/default/hosts/active/', "GET")
    hostConfig = json.loads(content)
    hosts = hostConfig['hostConfig']
    return hosts
#Find topology
def get_topology(xml):
    topology = json.loads(xml)
    nodes = topology['topology'][0]['node']
    links = topology['topology'][0]['link']
    return topology

    