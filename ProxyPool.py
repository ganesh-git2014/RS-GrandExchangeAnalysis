import urllib
import time
import requests



class ProxyPool(object):
    __ALIVE_PROXIES = []
    __PROXIES = []

    def __init__(self, proxy_list_filepath):
        self.__PROXIES = self.FileToList(proxy_list_filepath)


    #Takes a file path and converts the files contents to a list, file items must be new line seperated.
    #TODO: Add different split methods, i.e new line split, character split etc.
    def FileToList(self, file_path):
        with open(file_path) as pl:
            for p in pl.readlines():
                self.__PROXIES.append(p.rstrip('\n'))

            #self.__PROXIES = [i.rstrip('\n') for i in pl.readlines()]


    #Takes in a proxy list, checks if they're alive and returns a list of the working proxies.
    def ProxyTest(self, proxy_list=__PROXIES):
        alive_proxies = []
        for proxy in proxy_list:
            try:
                r = requests.get("http://www.google.com", proxies={"http": 'http://'+proxy},timeout=5)
                print "Appending proxy %s." % (proxy)
                alive_proxies.append(proxy)
            except:
                print "Skipping proxy %s" % (proxy)
                continue
        return alive_proxies

    #Takes in a list, prints it to a file on new lines for each item
    def ListToFile(self, dump_list, file_name, directory=""):
        with open(directory+file_name) as dump_file:
            for item in dump_list:
                dump_file.write("{0}{1}".format(item, '\n'))


p = ProxyPool('proxy_list')
print p.ProxyTest()





#ALIVE_PROXIES = ProxyTest(PROXIES)
#ListToFile(ALIVE_PROXIES, 'aliveproxies.txt', 'rs_logs/')



'''
print "Begining proxy cleanup."
for proxy in PROXIES:
    try:
        r = requests.get("http://www.google.com", proxies={"http": 'http://'+proxy},timeout=5)
        print "\nProxy alive! Adding {0} to alive list.".format(proxy)
        ALIVE_PROXIES.append(proxy)
    except Exception as e:
        print "\nWas not able to connect using proxy {0}".format(proxy)


print "\n Dumping alive proxies to file."
with open("rs_logs\\aliveproxies.txt", 'w') as ap:
    for p in ALIVE_PROXIES:
            ap.write(p+'\n')
'''


#NOT USING THIS METHOD

'''
proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
              "ftp"   : ftp_proxy
            }
'''
'''
with open("proxy_list") as pl:
    PROXY_DICT.update({'http' : i.rstrip('\n')} for i in pl.readlines())

for protocol, proxy in PROXY_DICT.iteritems():
    print protocol, proxy
'''

'''
for proxy in PROXIES:
    print "Trying HTTP proxy %s" % proxy
    try:
        result = urllib.urlopen("http://www.google.com", proxies={'http': proxy})
        print "Got URL using proxy %s" % proxy
        break
    except:
        print "Trying next proxy in 5 seconds"
        #time.sleep(5)
'''
