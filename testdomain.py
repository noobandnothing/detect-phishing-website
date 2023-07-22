import tldextract
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
        self.info()
    
    def info(self):
        print("url is : " +str(self.url))
        print("length is : " +str(self.length))
        print("protocol is : " +str(self.protocol))
        print("subdomain is : " +str(self.subdomain))
        print("domain is : " +str(self.domain))


v = testdomain("https://wiki.eclipse.org/ToString()_generation")