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

#Specific REST URLs
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'


h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

flowIdCounter = int(100)
hosts = restconf.get_active_hosts()

def get_topology(xml):
    topology = json.loads(xml)
    nodes = topology['topology'][0]['node']
    links = topology['topology'][0]['link']
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
    return switch#If an error is thrown here, you have to do a 'pingall' on mininet. This is caused by a bug in ODL 

def host_port(hosts, IP):
    for host in hosts:
        if host['networkAddress'] == IP:
            switchport = host['nodeConnectorId']
    return switchport#If an error is thrown here, you have to do a 'pingall' on mininet. This is caused by a bug in ODL

def find_ports(xml, headNode, tailNode):
    links = xml['topology'][0]['link']
    for link in links:
        if link['source']['source-node'] == headNode and link['destination']['dest-node'] == tailNode:
            portId = link['source']['source-tp']
            return portId
    return None
    
def add_sp_flows(shortest_path, srcIP, dstIP):
    flowId = flowIdCounter
    hardTimeOut, idleTimeOut = frontend.add_flow_gui(True)
    #Create flow rules to directly connected hosts from headnode and tailnode
    #HEAD
    flowName = shortest_path[0] + 'to' + srcIP
    outPutPort = host_port(hosts, srcIP)
    hostURL = confUrl+'opendaylight-inventory:nodes/node/'+shortest_path[0]+'/table/0/flow/'+str(flowId)
    #Because of a bug in ODL when updating flows we have to delete
    #any flows with the same flow id:
    restconf.delete(hostURL)
    flow = flow_rule_base(flowName, '0', str(flowId), hardTimeOut, idleTimeOut)
    flow = add_flow_action_sp(flow, outPutPort)
    flow = add_flow_match_sp(flow, srcIP)
    XMLstring = etree.tostring(flow,pretty_print=True,xml_declaration=True, encoding="utf-8", standalone=False )
    restconf.put(hostURL, XMLstring)
    #TAIL
    flowId = flowId + 1
    flowName = shortest_path[-1] + 'to' + dstIP
    outPutPort = host_port(hosts, dstIP)
    hostURL = confUrl+'opendaylight-inventory:nodes/node/'+shortest_path[-1]+'/table/0/flow/'+str(flowId)
    restconf.delete(hostURL)
    flow = flow_rule_base(flowName, '0', str(flowId), hardTimeOut, idleTimeOut)
    flow = add_flow_action_sp(flow, outPutPort)
    flow = add_flow_match_sp(flow, dstIP)
    XMLstring = etree.tostring(flow,pretty_print=True,xml_declaration=True, encoding="utf-8", standalone=False )
    restconf.put(hostURL, XMLstring)
    #For loop to create flow rules between all OF nodes end to end
    for i in range(len(shortest_path)-1):
        headNode = shortest_path[i]
        tailNode = shortest_path[i+1]
        flowId = flowId + 1
        #Forward Flow
        flowName = headNode + 'to' + tailNode + 'IPto' + dstIP
        outPutPort = find_ports(get_topology(restconf.get(findTopology)), shortest_path[i], shortest_path[i+1])
        forwardURL = confUrl+'opendaylight-inventory:nodes/node/'+shortest_path[i]+'/table/0/flow/'+str(flowId)
        restconf.delete(forwardURL)
        flow = flow_rule_base(flowName, '0', str(flowId), hardTimeOut, idleTimeOut)
        flow = add_flow_action_sp(flow, outPutPort)
        flow = add_flow_match_sp(flow, dstIP)
        forwardXMLstring = etree.tostring(flow,pretty_print=True,xml_declaration=True, encoding="utf-8", standalone=False )
        restconf.put(forwardURL, forwardXMLstring)
        #Backward Flow
        flowName = tailNode + 'to' + headNode + 'IPto' + srcIP
        outPutPort = find_ports(get_topology(restconf.get(findTopology)), shortest_path[i+1], shortest_path[i])
        backwardURL = confUrl+'opendaylight-inventory:nodes/node/'+shortest_path[i+1]+'/table/0/flow/'+str(flowId)
        restconf.delete(backwardURL)
        flow = flow_rule_base(flowName, '0', str(flowId), hardTimeOut, idleTimeOut)
        flow = add_flow_action_sp(flow, outPutPort)
        flow = add_flow_match_sp(flow, srcIP)
        backwardXMLstring =  etree.tostring(flow,pretty_print=True,xml_declaration=True, encoding="utf-8", standalone=False )
        restconf.put(backwardURL, backwardXMLstring)

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
    priority.text = "1"
    cookie = etree.SubElement(flow, "cookie")
    cookie.text = "0"
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
    
    #The Matches
    match = etree.SubElement(flow, "match")
    ethernet_match = etree.SubElement(match, "ethernet-match")
    ethernet_type = etree.SubElement(ethernet_match, "ethernet-type")
    type = etree.SubElement(ethernet_type, "type")
    type.text = "2048"
    return flow

def add_flow_match_sp(flow, destination):
    mat = flow.xpath('//match')[0]
    ipv4d = etree.SubElement(mat, 'ipv4-destination')
    ipv4d.text = destination
    return flow

def add_flow_action_sp(flow, port):
    action = flow.xpath('//action')[0]
    _act = etree.SubElement(action, 'output-action')
    onc = etree.SubElement(_act, 'output-node-connector')
    onc.text = port
    ml = etree.SubElement(_act, 'max-length')
    ml.text = '600'   
    return flow

def program():
    answer = frontend.main_menu()
    if answer == 'addFlow':
        answer = frontend.show_act_mat()
        if answer == 'addFlow':
            _node, _tableId, _flowId, _flowName, _hardTimeOut, _idleTimeOut = frontend.add_flow_gui(False)
            newFlow = flow_rule_base(_flowName, _tableId, _flowId, _hardTimeOut, _idleTimeOut)
            newFlow = frontend.add_actions(newFlow)
            newFlow = frontend.add_matches(newFlow)
            print etree.tostring(newFlow, pretty_print=True,xml_declaration=True, encoding="utf-8", standalone=False)
            print restconf.put(confUrl+'opendaylight-inventory:nodes/node/openflow:1/table/'+_tableId+'/flow/'+_flowId, etree.tostring(newFlow, xml_declaration=True, encoding="utf-8", standalone=False))
        elif answer == 'spfFlow':
            srcHost, destHost = frontend.get_ip_spf()
            shortest_path = get_sp(get_topology(restconf.get(findTopology)), host_switch(hosts, srcHost), host_switch(hosts, destHost))
            print "The shortest path between host %s and %s follows the following path:\n" % (srcHost,destHost) +str(shortest_path)
            print "Would you like to add this flow? (y/n) "
            answer = frontend.yes_no()
            if answer == 'y':
                add_sp_flows(shortest_path, srcHost, destHost)
                print "Your shortest path flow is added to the switches"
            else:
                pass
        else:
            pass
    elif answer == 'lookFlows':
        print json.dumps(frontend.view_flows(), indent=2)
        print '\n'
        frontend.main_menu()
    elif answer == 'delFlow':
        frontend.del_flow()
    else:
        pass
    program()
    
program()


       
        
