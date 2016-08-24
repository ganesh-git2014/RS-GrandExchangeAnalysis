import urllib
import time
import requests
from itertools import cycle



class ProxyPool(object):


    def __init__(self, proxy_list_filepath):
        self._ALIVE_PROXIES = []
        self._PROXIES = []
        self.FileToList(proxy_list_filepath)
        self.CycleProxies = cycle(self._PROXIES)
        

    #Takes a file path and converts the files contents to a list, file items must be new line seperated.
    #TODO: Add different split methods, i.e new line split, character split etc.
    def FileToList(self, file_path):
        with open(file_path) as pl:
            for p in pl.readlines():
                self._PROXIES.append(p.rstrip('\n'))

    #Takes in a proxy list, checks if they're alive and returns a list of the working proxies.
    def ProxyTest(self, proxy_list=None):
        if proxy_list is None:
            proxy_list = self._PROXIES

        alive_proxies = []
        for proxy in proxy_list:
            try:
                r = requests.get("http://www.google.com", proxies={"https": 'http://'+proxy},timeout=5)
                print "Appending proxy %s." % (proxy)
                self._ALIVE_PROXIES.append(proxy)
            except:
                print "Skipping proxy %s" % (proxy)

    #Takes in a list, prints it to a file on new lines for each item
    def ListToFile(self, file_name, dump_list=None, directory=None):
        if directory is None:
            directory = ""
        if dump_list is None:
            dump_list = self._ALIVE_PROXIES
        print "\nInitialising clean proxy dump"
        print "\nThere are %s clean proxies out of %s total" % \
            (len(self._ALIVE_PROXIES), len(self._PROXIES))
        with open(directory+file_name, 'w') as dump_file:
            for item in dump_list:
                dump_file.write("{0}{1}".format(item, '\n'))

    #retreives web content using proxy and returns the request object
    def GetNextProxy(self, url):
        proxy = self.CycleProxies.next()
        requestObj = requests.get(url, proxies={"https": 'http://'+proxy},timeout=5)
        return requestObj, proxy
    

if __name__ == "__main__":
    p = ProxyPool('proxy_list2')
    p.ProxyTest()
    p.ListToFile("clean_proxy_list2")
