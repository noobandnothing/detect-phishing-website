import tldextract
import socket
from urllib.parse import urlparse


class testdomain:
    def __init__(self,url):
        self.url = url
        self.length = len(self.url)
        self.protocol = str(urlparse(url).scheme)
        if self.protocol == "":
            raise Exception("Sorry, Invalid URL")
        self.subdomain, self.domain , self.tld = tldextract.extract(url)
        self.domain = self.domain +"."+ self.tld
        self.ip = self.__getip()
        self.valid = self.__IsValid()
        if not self.valid:
            print("Lets go out")            
        else:
            print("Lets continue")
        self.info()

    def __getip(self):
        try:
            return socket.gethostbyname(self.domain)
        except:
            # Domain name is not found
            return -1
    
    def __IsValid(self):
        try:
            socket.inet_aton(self.ip)
            return True
        except:
            # Domain name is not found
            return False
        
    def info(self):
        print("url is : " +str(self.url))
        print("length is : " +str(self.length))
        print("protocol is : " +str(self.protocol))
        print("subdomain is : " +str(self.subdomain))
        print("domain is : " +str(self.domain))
        print("IP is : " +str(self.ip))
        print("Valid is : " +str(self.valid))


v = testdomain("https://wikdafsasfasfi.eclipse.org/ToString()_generation")