#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth

# Global variables
serverIP = '192.168.231.246'
port = '8080'
container = 'default'
user = 'admin'
password = 'admin'

url = 'http://' + serverIP + ':' + port + '/controller/nb/v2'

getContainers = requests.get(url + '/containers', auth=(user,password))
print getContainers

getNodes = requests.get(url + '/connectionmanager/nodes', auth=(user,password))
print getNodes