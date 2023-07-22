import tldextract
import socket
import datetime
import whois
from urllib.parse import urlparse


class testdomain:
    def __init__(self,url):
        self.data = []
        self.url = url
        self.length = len(self.url)
        self.protocol = str(urlparse(url).scheme)
        if self.protocol == "":
            raise Exception("Sorry, Invalid URL")
        self.subdomain, self.domain , self.tld = tldextract.extract(url)
        if self.tld:
            self.domain = self.domain +"."+ self.tld
        self.ip = self.__getip()
        self.valid = self.__IsValid()
        if not self.valid:
            # Fill all 13 feature with 1 (false)
            for i in range(1, 13):
                self.data.append(1)          
        else:
            self.IsDomain = (self.ip != self.domain)
            self.age = self.__getage()
            self.expire = self.__get_domain_expiration()
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
    
    def __getage(self):
        try:
            return int((datetime.datetime.now() - whois.whois(self.domain).creation_date[0]).days)
        except:
            return -1
    
    def __get_domain_expiration(self):
        expiration_date = whois.whois(self.domain).expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date:
            days_left = (expiration_date - datetime.datetime.now()).days
            return days_left
        else:
            return -1


    def info(self):
        print("url is : " +str(self.url))
        print("length is : " +str(self.length))
        print("protocol is : " +str(self.protocol))
        print("subdomain is : " +str(self.subdomain))
        print("domain is : " +str(self.domain))
        print("IP is : " +str(self.ip))
        print("Valid is : " +str(self.valid))
        print("IsDomain is : " +str(self.IsDomain))
        print("Age is : " +str(self.age))
        print("Expire is : " +str(self.expire))


v = testdomain("https://google.com")