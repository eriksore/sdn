import restconf
import json
from lxml import etree
#Base URLs for Config and operational
baseUrl = 'http://192.168.231.246:8080'
confUrl = baseUrl + '/restconf/config/'
operUrl = baseUrl + '/restconf/operational/'

actionsTxt = open('actions.txt', 'r')
matchesTxt = open('matches.txt', 'r')

def view_flows():
    print 'On which switch do you want to look at the flows?'
    print 'Type in the number of the switch:'
    hosts = restconf.get_active_hosts()
    for host in hosts:
        print host['nodeId']
    answer = raw_input('> ')
    print 'Type in the number of the table you would like to look at:'
    answer2 = raw_input('> ')
    content = restconf.get('http://192.168.231.246:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:'+answer+'/table/'+answer2+'/')
    flows = json.loads(content)
    return flows['flow-node-inventory:table'][0]['flow-node-inventory:flow']
    
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
        main_menu()
    else:
        print 'You answered gibberish! Try again'
        main_menu()
    

def show_act_mat():
    print '\nYou chose to add a flow. Would you like to see your possible match and action fields? Type in number:'
    print '1. Show actions'
    print '2. Show instructions'
    print '3. Show both'
    print '4. Add flow straight away'
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
    else:
        print 'You answered gibberish! Try again'
        show_act_mat()
    return None

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

def add_actions(xml):
    print 'You need to add some actions to your flow'
    i = int(input('How many actions do you need to add? > '))
    actions = []
    print 'Write in your actions. Remember that they are: '
    print actionsTxt.read()
    while (i > 0):
        j = str(i)
        act = raw_input('Action '+j+' > ')
        if act == 'output-action':
            print 'You need to add some subelements to that one:'
            print 'physical port #, ANY, LOCAL, TABLE, INPORT, NORMAL, FLOOD, ALL, CONTROLLER'
            output_node_connector = raw_input('> ')
            print 'And max length:'
            max_length = raw_input('> ')
            action = xml.xpath('//action')[0]
            etree.SubElement(action, act)
            act = xml.xpath('//output-node-connector')[0]
            onc = etree.SubElement(act, 'output-node-connector')
            onc.text = output_node_connector
            ml = etree.SubElement(act, 'max-length')
            ml.text = max_length
        else:
            action = xml.xpath('//action')[0]
            etree.SubElement(action, act)
        i = i - 1
    return actions
    
def add_matches(xml):
    print 'You need to add some matches to your flow'
    i = int(input('How many matches do you need to add? > '))
    matches = []
    print 'Write in your matches. Remember that they are: '
    print matchesTxt.read()
    while (i > 0):
        j = str(i)
        matches.append(raw_input('Match '+j+' > '))
        i = i -1
    return matches
def main_menu():
    print "Welcome, what would you like to do? Type in number:"
    print "1. Add Flow"
    print "2. Look at flows"
    print "3. Delete flows"
    answer = raw_input('> ')
    if answer == '1':
        return 'addFlow'
    elif answer == '2':
        print 'You chose to look at flows'
        return 'lookFlows'
    elif answer == '3':
        print 'You want to delete a flow'
        return 'delFlow'
    else:
        print 'You answered gibberish! Try again'
        main_menu()
    return None


    
    
    

