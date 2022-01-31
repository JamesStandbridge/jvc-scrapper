import sys, time, threading
from jvc_api import JVC

frequency=5

forums_to_scrap = (
	{"url": "/0-51-0-1-0-1-0-blabla-18-25-ans.htm", "search": "Elder Ring"},
	{"url": "/0-25075-0-1-0-1-0-dark-souls.htm", "search": None},
	{"url": "/0-30226-0-1-0-1-0-dark-souls-ii.htm", "search": None},
	{"url": "/0-3003024-0-1-0-1-0-dark-souls-iii.htm", "search": None},
	{"url": "/0-3016975-0-1-0-1-0-elden-ring.htm", "search": None}
)

def execute(forum, thread_id):
	client = JVC("", forum['url'])
	while True:
		#print("Thread {}".format(thread_id))
		print(client.getLastTopic(1, forum['search']).url)
	time.sleep(frequency)
	clearOutput()

i = 0
for forum in forums_to_scrap:
	i += 1
	threading.Thread(
		target=execute,
	    args=(forum,i)
	).start()
