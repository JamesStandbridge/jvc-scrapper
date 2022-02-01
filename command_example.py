#!/usr/bin/python

import sys, time, threading
from jvc_api import JVC

print('Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))

url = sys.argv[1]

if(len(sys.argv) > 2):
	search = sys.argv[2]
else:
	search = None

client = JVC("", url)
topic = client.getLastTopic(1, search)

print(topic.url)
print(topic.title)