import tldextract
import socket
import datetime
import whois
import requests
import time


from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
            self.google_index = self.__get_googleindex()
            ###############            ###############    ###############
            self.https = self.__check_https()
            self.url_anchor = self.__get_url_anchor()
            self.url_prefixandsuffix = self.__get_url_prefixandsuffix()
            tmp = self.__get_webtraffic_pagerank()
            self.pagerank = tmp[0]
            self.webtraffic = tmp[1]
            self.requesturl =  self.__get_requesturl()
            self.urlmeta = self.__get_url_meta()

            
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
    
    def __get_googleindex(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(f'{"https://www.google.com/search?q="}'+f'{self.domain}', headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return int(soup.select_one("#result-stats").text.strip().split(' ')[1].replace(",",""))

    def __check_https(self):
        if self.protocol != "https":
            return 1
        else:
            try:
                response = requests.head(self.url)
                return int(response.url.startswith("https://"))*-1
            # There is more to check cert
            except requests.exceptions.RequestException:
                return 1

    # GET anchor######################
    
    # Function to calculate the percentage of anchor tags that do not link to any webpage
    def __get_url_anchor(self):
        # LINUX DRIVER
        #geckodriver_path = ' '  # Replace with the actual path
        #driver = webdriver.Firefox(executable_path=geckodriver_path)
        driver = webdriver.Chrome(options = webdriver.ChromeOptions())
        driver.get(self.url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')

        total_anchors = 0
        no_link_anchors = 0
        
        for tag in soup.find_all('a'):
            total_anchors += 1
                
            anchor_url = tag.get('href')
            if anchor_url in ['#', '#skip', 'JavaScript'] or tldextract.extract(anchor_url)[1] not in self.domain:
                no_link_anchors += 1

        # Calculate the percentage of anchor tags that do not link to any webpage
        no_link_percentage = (no_link_anchors / total_anchors) * 100 if total_anchors > 0 else 0
        if no_link_percentage < 31:
            return -1
        elif 31 <= no_link_percentage <= 67:
            return 0
        else:
            return 1
        
    def __get_url_prefixandsuffix(self):
        if "-" in self.domain or "-" in self.subdomain:
            return 1
        else:
            return -1
        
    ##################################
    
    def __get_webtraffic_pagerank(self):
        # LINUX DRIVER
        #geckodriver_path = ' '  # Replace with the actual path
        #driver = webdriver.Firefox(executable_path=geckodriver_path)
        driver = webdriver.Chrome(options = webdriver.ChromeOptions())
        if self.subdomain:
            target = 'https://www.similarweb.com/website/'+self.subdomain+"."+self.domain+'/#overview'
        else:
            target = 'https://www.similarweb.com/website/'+self.domain+'/#overview'
        driver.get(target)
        time.sleep(10)
        current_url = driver.current_url
        if current_url != target:
            driver.quit()
            return [1,1]
        html = driver.page_source

        driver.quit()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html,'html.parser')
        if len(soup.find_all('div', class_='search-results__no-data')) == 1 :
            return [1,1]
        another = BeautifulSoup(str(soup.find_all('div', class_='engagement-list__item')),'html.parser')
        x = str(another.find_all('p', class_='engagement-list__item-value')[0])
        x = x.split('>')[1].split('<')[0].replace("'","").replace(",","").replace("-","")
        if "B" in x:
            x = x.replace("B","")
            x = float(x)
            x = x * 1000000000
        elif "M" in x:
            x = x.replace("M","")
            x = float(x)
            x = x * 1000000
        elif "K" in x:
            x = x.replace("K","")
            x = float(x)
            x = x * 1000

        webtraffic = 0
        if  x == ' ':
            return [1,1]
        else:
            webtraffic = float(x)
        
            page_rank = str(soup.find_all('p', class_='wa-rank-list__value')[0]).split('>')[-2].split('<')[0].replace("'","").replace(",","").replace("-","")
            if page_rank == " ":
                page_rank = 0
            else:
                page_rank = float(page_rank)

            arr = []
            if page_rank == 0:
                arr.append(1)
            else:
                arr.append(-1)

            if webtraffic < 100000:
                arr.append(1)
            else:
                arr.append(-1)
        
            return arr[0],arr[1]
    ##################################
    def __get_requesturl(self):
        total_links = 0
        links_in_domain = 0
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all(['img', 'source']):
            if tag.get('src'):
                link = tag.get('src')
                if str(urlparse(link).scheme) == '' or tldextract.extract(link)[1]  is None:
                    links_in_domain +=1
                    total_links +=1
                elif tldextract.extract(link)[1] in self.domain:
                    links_in_domain +=1
                    total_links +=1
                else:
                    total_links +=1

                link_percentage = (total_links-links_in_domain / total_links) * 100 if total_links > 0 else 0
                if link_percentage < 22:
                    return -1
                elif 22 <= link_percentage <= 61:
                    return 0
                else:
                    return 1
        return -1 
    ##################################
    def __get_url_meta(self):
        # LINUX DRIVER
        #geckodriver_path = ' '  # Replace with the actual path
        #driver = webdriver.Firefox(executable_path=geckodriver_path)
        driver = webdriver.Chrome(options = webdriver.ChromeOptions())
        driver.get(self.url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        
        total_links = 0
        links_in_tags = 0

        # Count total links and links in <Meta>, <Script>, and <Link> tags
        for tag in soup.find_all(['meta', 'script', 'link']):
            if tag.get('href') or tag.get('src'):
                total_links += 1
                if tag.name in ['meta', 'script', 'link'] and tag.get('href') and tag.get('href').startswith('http'):
                    links_in_tags += 1

        # Calculate the percentage of links in tags
        link_percentage = (links_in_tags / total_links) * 100 if total_links > 0 else 0
        if link_percentage < 17:
            return -1
        elif 17 <= link_percentage <= 81:
            return 0
        else:
            return 1
    ##################################
    ##################################

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
        print("Google Index is : " +str(self.google_index))
        print("HTTPS is : " +str(self.https))
        print("URL Anchor is : " +str(self.url_anchor))
        print("URL Prefix-Suffix is : " +str(self.url_prefixandsuffix))
        print("Page Rank is : " +str(self.pagerank))
        print("Web Traffic is : " +str(self.webtraffic))
        print("Request url is : " +str(self.requesturl))
        print("Url Meta is : " +str(self.urlmeta))


v = testdomain("https://google.com")