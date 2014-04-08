import sys
import json
import httplib2

#Base URLs for Config and operational
baseUrl = 'http://192.168.231.246:8080'
confUrl = baseUrl + '/restconf/config/'
operUrl = baseUrl + '/restconf/operational/'

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

#Functions for  
def get(h, url):
    resp, xml = h.request(
        url,
        method = "GET",
        headers = {'Content-Type' : 'application/xml'}
        )
    return xml
def put(h, url, body):
    resp, content = h.request(
        url, 
        method = "PUT",
        body = body,
        headers = {'Content-Type' : 'application/xml', 'Accept':'application/xml'}
        )
    return resp, content
def del(h, url, node, table, flow):
    resp, content = h.request(
        url,
        method = "DELETE"
        )
    