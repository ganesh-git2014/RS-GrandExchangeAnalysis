import json, requests, time, sys, os

items = {}
dump_dir = "rs_logs/"
timeDate = time.asctime()
log_name = "rs_dump-%s.log" % (timeDate.replace(":","_"))

with open("Runescape-items.txt") as file:
	for line in file.readlines():
		a = line.split('\t')
		items.update({a[0] : a[1].rstrip("\n")})


def GetItemInfo(itemID):
    url = "http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item="
    postUrl = url+itemID
    r = requests.get(postUrl)
    c = json.loads(r.content)

    _name = c['item']['name']
    _type= c['item']['type']
    _trend = c['item']['current']['trend']
    _price = c['item']['current']['price']
    _CurrentDateTime = time.asctime()
    return '%s Name="%s" Type="%s" Trend="%s" Price="%s"\n' \
    		 % (_CurrentDateTime, _name,_type,_trend,_price), \
    		  r.status_code, r.text, postUrl



class progress:
	def __init__(self, nItems, sleepAt):
		self.nItems = nItems
		self.sleepAt = sleepAt
		self.loops = 0

	'''
	#get milli seconds
	def GML():
		return int(round(time.time() * 1000))

	def TimeProgress(self):
		#startTime = time.strftime('%X')
		millis = 
		startTime = 
	'''
	def printProgress(self):
		'''
		if self.loops == self.sleepAt:
			sys.stdout.write("Sleeping for 3 seconds...\r")
			sys.stdout.flush()
			time.sleep(3)
			self.loops = 0
		'''
		sys.stdout.write('{0} out of {1} items left to be downloaded{2}'.format(self.nItems, len(items), '\b' * 100))
		sys.stdout.flush()
		self.nItems -= 1
		self.loops += 1



amount = len(items)
unfound = []
p = progress(len(items), 100)

with open(dump_dir+log_name, 'w') as dumpFile:
    print "Initializing dump."
    print "Dumping %s Items" % (len(items))
    print "\nDownloading latest item prices...\n"
    for iid, item in items.iteritems():
        try:
        	q, i, t, j = GetItemInfo(iid)
        	#dumpFile.write(GetItemInfo(iid))
        	dumpFile.write(q)
        	p.printProgress()
        	time.sleep(2.5)
        except Exception:
        	#print j
        	#print e
        	#print i
        	#print t
        	print "\nskipping item %s - %s" % (iid, item)
        	unfound.append(iid + ' ' + item)
        	p.nItems -= 1
        	continue

print "\nDump complete."
print unfound

        

#def dumpStatus():

