import restconf

def view_flows():
    print 'On which switch do you want to look at the flows?'
    print 'Type in the number of the switch:'
    hosts = get_active_hosts()
    for host in hosts:
        print host['nodeId']
    answer = raw_input('> ')
    print 'Type in the number of the table you would like to look at:'
    answer2 = raw_input('> ')
    content = restconf.get(h, 'http://192.168.231.246:8080/restconf/config/opendaylight-inventory:nodes/node/openflow:'+answer+'/table/'+answer2+'/')
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
    if answer == 'y:
        mainmenu()
    elif answer == 'n':
        mainmenu()
    else:
        print 'You answered gibberish! Try again'
        mainmenu()
    

def show_act_mat():
    actionsTxt = open('actions.txt', 'r')
    matchesTxt = open('matches.txt', 'r')
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

def mainmenu():
    print "Welcome, what would you like to do? Type in number:"
    print "1. Add Flow"
    print "2. Look at flows"
    print "3. Delete flows"
    answer = raw_input('> ')
    if answer == '1':
        show_act_mat()
    elif answer == '2':
        print 'You chose to look at flows'
        return 'lookFlows'
    elif answer == '3':
        print 'You want to delete a flow'
        return 'delFlow'
    else:
        print 'You answered gibberish! Try again'
        mainmenu()
    return None

