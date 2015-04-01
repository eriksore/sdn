import restconf
import json
from lxml import etree
#Base URLs for Config and operational
baseUrl = 'http://192.168.231.255:8080'
confUrl = baseUrl + '/restconf/config/'
operUrl = baseUrl + '/restconf/operational/'
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
actionsTxt = open('actions.txt', 'r')
matchesTxt = open('matches.txt', 'r')
#Function to view flows in the topology
def view_flows():
    print 'On which switch do you want to look at the flows?'
    print 'Type in the number of the switch (as listed):'
    nodes = restconf.get_topology(restconf.get(findTopology))['topology'][0]['node']
    for node in nodes:
        print node['node-id']
    answer = raw_input('> ')
    print 'Type in the number of the table you would like to look at:'
    answer2 = raw_input('> ')
    content = restconf.get('http://192.168.231.250:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:'+answer+'/table/'+answer2+'/')
    flows = json.loads(content)
    return flows['flow-node-inventory:table'][0]['flow-node-inventory:flow']
#User input yes or no
def yes_no():
    answer = raw_input(' >')
    return answer
#Function to delete a flow manually    
def del_flow():  
    print 'On which node do you want to delete a flow?'
    node = raw_input('> ')
    print 'In which table of node '+node+' do you want to delete a flow?'
    table = raw_input('> ')
    print 'What is the flow id for the flow you want to delete?'
    flowId = raw_input('> ')
    print 'Do you really want to delete flow '+flowId+' in table '+table+' on node '+node+' ? (y/n)'
    answer = raw_input('> ')
    if answer == 'y':
        url = confUrl+'opendaylight-inventory:nodes/node/openflow:'+node+'/table/'+table+'/flow/'+flowId
        print restconf.delete(url)
    elif answer == 'n':
        del_flow()
    else:
        print 'You answered gibberish! Try again'
        del_flow()
#User input for host source and destination addresses
def get_ip_spf():
    srcHost = raw_input('Type IP of Source host > ')
    destHost = raw_input('Type IP of destination host >')
    return srcHost, destHost
    

def show_act_mat():
    print '\nYou chose to add a flow. Would you like to see your possible match and action fields? Type in number:'
    print '1. Show actions'
    print '2. Show instructions'
    print '3. Show both'
    print '4. Add manual flow'
    print '5. Add SPF flow'
    answer = raw_input('> ')
    if answer == '1':
        print actionsTxt.read()
        show_act_mat()
    elif answer == '2':
        print matchesTxt.read()
        show_act_mat()
    elif answer == '3':
        print actionsTxt.read()
        print matchesTxt.read()
        show_act_mat()
    elif answer == '4':
        return 'addFlow'
    elif answer == '5':
        return 'spfFlow'
    else:
        print 'You answered gibberish! Try again'
        show_act_mat()
    return None
#User input for flow specifics
def add_flow_gui():
    print 'You chose to add a flow. Please answer these parameters'
    print 'First the RESTConf specific parameters. E.g: /opendaylight-inventory:nodes/node/openflow:1/table/0/flow/1'
    node = raw_input('Node? > ')
    table = raw_input('Table? > ')
    flowId = raw_input('Flow number? > ')
    print 'Then the flow specifics:'
    flowName = raw_input('FlowName? > ')
    hardTimeOut = raw_input('Hard Time Out? > ') 
    idleTimeOut = raw_input('Idle Time Out? > ')
    return node, table, flowId, flowName, hardTimeOut, idleTimeOut

        
#User input for actions  
def add_actions(xml):
    print 'You need to add some actions to your flow'
    i = int(input('How many actions do you need to add? > '))
    print 'Write in your actions. Remember that they are: '
    print actionsTxt.read()
    while (i > 0):
        j = str(i)
        act = raw_input('Action '+j+' > ')
        if act == 'output-action':
            print '    You need to add some subelements to that one:'
            print '    physical port #, ANY, LOCAL, TABLE, INPORT, NORMAL, FLOOD, ALL, CONTROLLER'
            output_node_connector = raw_input('    > ')
            print '    And max length:'
            max_length = raw_input('    > ')
            action = xml.xpath('//action')[0]
            _act = etree.SubElement(action, act)
            onc = etree.SubElement(_act, 'output-node-connector')
            onc.text = output_node_connector
            ml = etree.SubElement(_act, 'max-length')
            ml.text = max_length
        else:
            action = xml.xpath('//action')[0]
            etree.SubElement(action, act)
        i = i - 1
    return xml
#User input for matches   
def add_matches(xml):
    mat = xml.xpath('//match')[0]
    print 'You need to add some matches to your flow'
    i = int(input('How many matches do you need to add? > '))
    print 'Write in your matches. Remember that they are: '
    print matchesTxt.read()
    while (i > 0):
        j = str(i)
        match = raw_input('Match '+j+' > ')
        if match == 'ethernet-match':
            print '    The default Ethernet type is 2048. Do you need to change this? (y/n)'
            answer = raw_input('    >')
            if answer == 'y':
                e_type = xml.xpath('//ethernet-type')[0]
            else:
                pass
            print '    You need to add some subelements to that one:'
            print '    Source address? (y/n)?'
            ethernet_match = xml.xpath('//ethernet-match')[0]
            answer = raw_input('    >')
            if answer == 'y':
                es = etree.SubElement(ethernet_match, 'ethernet-source')
                es_address = etree.SubElement(es, 'address')
                address = raw_input('    Address >')
                es_address.text = address   
            else:
                pass
            print '    Destination address? (y/n)'
            answer == raw_input('    >')
            if answer == 'y':
                ed = etree.SubElement(ethernet_match, 'ethernet-destination')
                ed_address = etree.SubElement(ed, 'address')
                address = raw_input('    Address >')
                ed_address.text = address
            else:
                pass
        elif match == 'ipv4-destination':
            answer = raw_input('    Address >')
            ipv4d = etree.SubElement(mat, match)
            ipv4d.text = answer
        elif match == 'ipv4-source':
            answer = raw_input('    Address >')
            ipv4s = etree.SubElement(mat, match)
            ipv4s.text = answer
        elif match == 'tcp-source-port':
            answer = raw_input('    Address >')
            tcpsp = etree.SubElement(mat, match)
            tcpsp.text = answer
        elif match == 'tcp-destination-port':
            answer = raw_input('    Address >')
            tcpdp = etree.SubElement(mat, match)
            tcpdp.text = answer
        elif match == 'udp-source-port':
            answer = raw_input('    Address >')
            udpsp = etree.SubElement(mat, match)
            udpsp.text = answer
        elif match == 'udp-destination-port':
            answer = raw_input('    Address >')
            udpdp = etree.SubElement(mat, match)
            udpdp.text = answer
        elif match == 'vlan-match':
            answer = raw_input('    VLAN ID >')
            vlanm = etree.SubElement(mat, match)
            vlanid = etree.SubElement(match, 'vlan-id')
            vlanid_ = etree.SubElement(vlanid, 'vlan-id')
            vlanid_.text = answer
            vlanidpresent = etree.SubElement(_vlanid, 'true')
            answer = raw_input('    VLAN PCP >')
            vlanpcp = etree.SubElement(match, 'vlan-pcp')
            vlanpcp.text = answer
        elif match == 'tunnel':
            answer = raw_input('    Tunnel ID >')
            tunnel = etree.SubElement(mat, match)
            tunnelid = etree.SubElement(match, 'tunnel-id')
            tunnelid.text = answer
        else:
            pass
        i = i -1
    return xml
#User input used when moving a tunnel
def move_flow():
    print 'Between which hosts do you want to move the tunnel?'
    srcHost = raw_input('Source host >')
    destHost = raw_input('Destination host >')
    print 'Choose node to exclude from SPF calculation:'
    nonSwitch = raw_input(' >')
    return nonSwitch, srcHost, destHost

#Main meno for the UI
def main_menu():
    print "Welcome, what would you like to do? Type in number:"
    print "1. Add Flow"
    print "2. Look at flows"
    print "3. Delete flows"
    print "4. Move a flow"
    answer = raw_input('> ')
    if answer == '1':
        return 'addFlow'
    elif answer == '2':
        print 'You chose to look at flows'
        return 'lookFlows'
    elif answer == '3':
        print 'You want to delete a flow'
        return 'delFlow'
    elif answer == '4':
        print 'You want to move a flow'
        return 'moveFlow'
    else:
        print 'You answered gibberish! Try again'
        main_menu()
    


    
    
    

