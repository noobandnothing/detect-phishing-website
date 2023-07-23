import tldextract
import socket
import datetime
import whois
import requests
import time
        
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
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
            #self.expire = self.__get_domain_expiration()
            # ###############            ###############    ###############
            tmp = self.__getsomeinfo()
            if type(tmp) == type(1) :
                raise Exception("Sorry, there is problem "+str(tmp))
            else:
                self.obj_soup , self.resp_url = self.__getsomeinfo()
            # ###############            ###############    ###############
            self.HTTPS = self.__check_https()
            self.AnchorURL = self.__get_url_anchor()
            self.PrefixSuffix = self.__get_url_prefixandsuffix()
            self.PageRank,self.WebsiteTraffic = self.__get_webtraffic_pagerank()
            # ###############           ###############    ################
            if len(self.subdomain.split(".")) == 1:
                self.SubDomains = -1
            elif len(self.subdomain.split(".")) == 2:
                self.SubDomains = 0
            else:
                self.SubDomains = 1
            # ###############           ###############    ################
            self.RequestURL =  self.__get_requesturl()
            self.LinksInScriptTags = self.__get_url_meta()
            self.ServerFormHandler = self.__get_SFH()
            self.GoogleIndex = self.__get_googleindex()
            self.AgeofDomain = self.__getage()
            # ###############           ###############    ################
            if self.IsDomain:
                self.UsingIP = -1
            else:
                self.UsingIP = 1
            
        #     ################################################################
            self.__getbrief()
    
    def __IsValid(self):
        try:
            socket.inet_aton(self.ip)
            return True
        except:
            # Domain name is not found
            return False
    
    def __getage(self):
        try:
            age =  int((datetime.datetime.now() - whois.whois(self.domain).creation_date[0]).days)
            if age >= 6 :
                return -1
            else:
                return 1
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
        response.close()
        tmp = int(soup.select_one("#result-stats").text.strip().split(' ')[1].replace(",",""))
        if tmp :
            return -1
        else:
            return 1
    
    def __getsomeinfo(self):
        #GSI
        tmp = []
        try:
            # response = requests.post(self.url)
            # tmp.append(BeautifulSoup(response.text, 'html.parser'))
            # tmp.append(response.url)
            # response.close()
            # Use this way to prevent blocking robot
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu') 
            driver = webdriver.Chrome(options = options)
            driver.get(self.url)
            time.sleep(5)
            html = driver.page_source
            tmp.append(BeautifulSoup(html, 'html.parser'))
            tmp.append(driver.current_url)
            driver.quit()
            return tmp
        except Exception as err: 
            if 'InvalidSchema' in str(type(err)):
                # it redirect to none or unkown dest
                return 0
            elif 'ConnectionError' in str(type(err)) or 'SSLError' in str(type(err)):
                # Connection error
                return 1
            else:
                raise Exception("Error GSI: " +str(err))
            

    def __check_https(self):
        if self.protocol != "https":
            return 1
        else:
            try:
                return int(self.resp_url.startswith("https://"))*-1 
            # There are more to check cert
            except requests.exceptions.RequestException:
                return 1

    def __getip(self):
        try:
            return socket.gethostbyname(self.domain)
        except:
            # Domain name is not found
            return -1
        
    # GET anchor######################
    
    # Function to calculate the percentage of anchor tags that do not link to any webpage
    def __get_url_anchor(self):
        #import copy
        #soup = copy.deepcopy(self.obj_soup)

        total_anchors = 0
        no_link_anchors = 0
        
        for tag in self.obj_soup.find_all('a'):
            total_anchors += 1

            anchor_url = tag.get('href')
            if anchor_url:
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
        #GWTPR
        try:
            # LINUX DRIVER
            #geckodriver_path = ' '  # Replace with the actual path
            #driver = webdriver.Firefox(executable_path=geckodriver_path)
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu') 
            driver = webdriver.Chrome(options = options)
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
        except Exception as err: 
            raise Exception("Error GWTPR: Please try again " +str(err))
    ##########HERE####HERE############
    def __get_requesturl(self):
        total_links = 0
        links_in_domain = 0
        try:
            for tag in self.obj_soup.find_all(['img', 'source']):
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
        except Exception as err: 
            if 'InvalidSchema' in str(type(err)):
                # it redirect to none or unkown dest
                return 1
            elif 'ConnectionError' in str(type(err)) or 'SSLError' in str(type(err)):
                # Connection error
                return 0

        
        return -1
    ##################################
    def __get_url_meta(self):
        total_links = 0
        links_in_tags = 0

        # Count total links and links in <Meta>, <Script>, and <Link> tags
        for tag in self.obj_soup.find_all(['meta', 'script', 'link']):
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
    def __get_SFH(self):
        try:
            sfh_subdomain, sfh_domain , sfh_tld = tldextract.extract(self.resp_url)
            if self.IsDomain:
                if sfh_domain+"."+sfh_tld == self.domain:
                    return -1
                else:
                    return 0
            elif sfh_subdomain == self.domain:
                return -1
            else:
                return 0
        except Exception as err: 
            if 'InvalidSchema' in str(type(err)):
                # it redirect to none or unkown dest
                return 1
            elif 'ConnectionError' in str(type(err)) or 'SSLError' in str(type(err)):
                # Connection error
                return 0
            else:
                return 1
    ##################################
    # def __get_url_links_Pointing_page(self,url):
    #     try:
    #         response = requests.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         links = soup.find_all('a')
    #         # Count the number of links pointing to the webpage
    #         num_links = 0
    #         for link in links:
    #             href = link.get('href')
    #             if href and self.domain in href:
    #                 num_links += 1
    #         if num_links == 0:
    #             return 1
    #         elif num_links > 0 and num_links <= 2:
    #             return 0
    #         else:
    #             return -1

    #     except requests.exceptions.RequestException as e:
    #         print("Error:", e)
    #         return None
    ##################################

    def __getbrief(self):
        import os
        if os.path.isfile('DTM.pkl'):
            from joblib import load
            clf = load('DTM.pkl')
            for attribute_name in clf.feature_names_in_:
                self.data.append(getattr(self, attribute_name.replace("-","")))
        else:
            return None
            



#test = testdomain("https://google.com")

