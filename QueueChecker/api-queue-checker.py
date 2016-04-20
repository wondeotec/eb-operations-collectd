#!/usr/bin/env python
import urllib2
import json
import ConfigParser
import os

Config = ConfigParser.ConfigParser()
dir = os.path.dirname(__file__)
path = os.path.join(dir, "config/config-queue-checker.ini")
Config.read(path)


queue_name = Config.get('queue', 'name')
queue_password = Config.get('queue', 'password')
queue_virtual_host = Config.get('queue', 'virtual_host')
queue_host = Config.get('queue', 'host')
queue_user = Config.get('queue', 'user')
queue_port = int(Config.get('queue', 'port'))
interval = int(Config.get('librato', 'interval'))
hostname = Config.get('librato', 'host')

url = 'http://localhost:%s/api/queues/%s/%s' % (queue_port, queue_virtual_host, queue_name)

# simple wrapper function to encode the username & pass
def encodeUserData(user, password):
    return "Basic " + (user + ":" + password).encode("base64").rstrip()

# create the request object and set some headers
req = urllib2.Request(url)
req.add_header('Accept', 'application/json')
req.add_header("Content-type", "application/json")
req.add_header('Authorization', encodeUserData(user=queue_user, password=queue_password))
# make the request and print the results
res = urllib2.urlopen(req)
res = json.loads(res.read())

print 'PUTVAL \"%s/%s/gauge-status\" interval=%s N:%s' % (hostname, queue_name, interval, res['messages'])
