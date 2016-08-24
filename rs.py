from prettify import cPrint
from ProxyPool import ProxyPool
import json
import requests
import time
import sys


SERVICES_API = "http://services.runescape.com/m=itemdb_rs/api/"

multipliers = {'k' : 1000, 'm' : 1000000, 'b' : 1000000000}

INDEX = {}
PRICE_DATA = []

timeDate = time.asctime()
LOG_DIR = 'rs_logs/'
LOG_FILE = "rs_dump-%s.log" % (timeDate.replace(":", "_"))

proxy_pool = ProxyPool('proxy_list')

def SuffixUnpack(price):
    suffix = str(price)[-1]
    if suffix in multipliers:
        temp = int(float(price[:-1]) * multipliers[suffix])
        price = str("{:,}".format(temp))
    return price

def LiveStatus(mType, message):
    sys.stdout.write(cPrint(mType, "{: <120}".format(message), 'r'))
    time.sleep(0.1)
    sys.stdout.flush()

def ProcessCategory(category, jsonObj):
    INDEX[category] = []
    for alpha in jsonObj['alpha']:
        if alpha['items'] > 0:
            INDEX[category].append(alpha['letter'])

def ProcessPage(jsonObj):
    for item in jsonObj['items']:
        _name = item['name']
        _type= item['type']
        _trend = item['current']['trend']
        _price = SuffixUnpack(item['current']['price'])
        PRICE_DATA.append('Name="{0}" Type="{1}" Trend="{2}" Price="{3}"'.format(
                           _name,     _type,     _trend,     _price))

def UpdateIndex():
    BASE_URL = SERVICES_API + "catalogue/category.json"

    # Consider future-proofing the range
    for category in range(38): #TODO: 38
        url = BASE_URL + "?category={0}".format(category)

        try:
            r, proxyUsed = proxy_pool.GetNextProxy(url)
            c = json.loads(r.content)
            ProcessCategory(category, c)

            #Verbose Mode
            LiveStatus('p','Updating index for category {0}'.format(category))
            print "\t", proxyUsed, r
        except Exception as e:
            cPrint('w', "Unable to load category {0}: {1}".format(category, url))
            print "\t", proxyUsed, r, r.content
            #Verbose Mode
            cPrint('c', "Reason: {0}".format(e.message))

    cPrint('s','Index Update Complete.')

def FetchPrices(cat, alphas):
    BASE_URL = SERVICES_API + "catalogue/items.json"

    for letter in alphas:
        # Consider future-proofing the range
        for page in range(99): ## TODO: 99
            url = BASE_URL + "?category={0}&alpha={1}&page={2}".format(cat, letter, page)
            try:
                r, proxyUsed = proxy_pool.GetNextProxy(url)
                c = json.loads(r.content)
                print "\t", proxyUsed, r
                if c['items']:
                    #Verbose Mode
                    LiveStatus('p','Fetching Prices category {0} letter {1} page {2}'.format(category, letter, page))
                else:

                    LiveStatus('w','Reached last page, proceeding to next letter')
                    break
                ProcessPage(c)
                #Debugging page break mech
                #print "\nyes" + str(len(c['items'])) if c['items'] > 0 else "\nNo" + str(c)
            except Exception as e:
                cPrint('w', "Unable to load items category {0} letter {1} page {2}: {3}".format(category, letter, page, url))
                print e.message
                print "\t", proxyUsed, r

def FileDump():
    cPrint('p','Initialising Dump.')
    with open(LOG_DIR + LOG_FILE, 'w') as dump_file:
        for item in PRICE_DATA:
            dump_file.write(item+'\n')
            LiveStatus('p','Dumping: {0}'.format(item))

    cPrint('s','Dumped {0} Successfully.'.format(len(PRICE_DATA)))


# Main
cPrint('p', "Updating Index")
UpdateIndex()


for category, alphas in INDEX.iteritems():
    FetchPrices(category, alphas)
    break
    #cPrint('p','Sleeping for 5 minutes')
    #time.sleep(300)

FileDump()



'''

for i in range(10):
    try:
        r = proxy_pool.GetNextProxy('http://www.google.com')
        print r
    except Exception as e:
        print "woops"
'''