import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
resp, content = h.request('http://192.168.231.246:8080/controller/nb/v2/statistics/default/flow', "GET")
allFlowStats = json.loads(content)
flowStats = allFlowStats['flowStatistics']

for fs in flowStats:
    print "\nSwitch ID : " + fs['node']['id']
    print '{0:8} {1:8} {2:5} {3:15}'.format('Count', 'Action', 'Port', 'DestIP')
    for aFlow in fs['flowStatistic']:
        count = aFlow['packetCount']
        actions = aFlow['flow']['actions'] 
        actionType = ''
        actionPort = ''
        #print actions
        if(type(actions) == type(list())):
            actionType = actions[0]['type']
            actionPort = actions[0]['port']['id']
        else:
            actionType = actions['type']
            actionPort = actions['port']['id']
        dst = aFlow['flow']['match']['matchField'][0]['value']
        print '{0:8} {1:8} {2:5} {3:15}'.format(count, actionType, actionPort, dst)
