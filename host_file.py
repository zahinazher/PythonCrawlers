##************Copyrights EBRYX***********##
## OWNER: Zahin Azher Rashid
## Dependencies: BeautifulSoup
##*************Thank You***************##
from BeautifulSoup import BeautifulSoup
import urllib2
import logging
import re

class host_file:
	UAcount = 0
	def __init__(self):
		#logging.basicConfig(filename='/tmp/logs.log')
		self.logger = logging.getLogger('host_file')
		self.url = 'http://www.hosts-file.net'
		self.userAgents = ["Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0\
         Safari/537.36", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko)\
          Chrome/15.0.872.0 Safari/535.2",
                           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko)\
                            Chrome/14.0.792.0 Safari/535.1",
                           "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
                           "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
                           "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
                           "Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko",
                           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                           "Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.14",
                           "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
                           "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
                           "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.8\
                            (KHTML, like Gecko) Safari/312.6",
                           "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/125.2\
                            (KHTML, like Gecko) Safari/125.7",
                           "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fi-fi)\
                            AppleWebKit/420+ (KHTML, like Gecko) Safari/419.3",
                           "amaya/11.1 libwww/5.4.0",
                           "amaya/9.52 libwww/5.4.0",
                           "Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20120325 Firefox/11.0 AvantBrowser/Tri-Core",
                           "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20120325 Firefox/11.0 AvantBrowser/Tri-Core",
                           "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120515 Firefox/12.0 AvantBrowser/Tri-Core",
                           "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.3) Gecko/20041007 Epiphany/1.4.7",
                           "Mozilla/5.0 (X11; U; Linux i686; en; rv:1.8.1.12)\
                            Gecko/20080208 (Debian-1.8.1.12-2) Epiphany/2.20",
                           "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.1)\
                            Gecko/20060314 Flock/0.5.13.2",
                           "Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1",
                           "Lynx/2.8.6rel.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.6.3",
                           "Lynx/2.8.5dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.7a",
                           "Lynx/2.8.3dev.6 libwww-FM/2.14"]
		
	# Each time when this method is called it uses a different User-Agent
	def get_data(self,urlDict):
		try :
			request = urllib2.Request(self.url)
			request.add_header('User-agent', self.userAgents[self.UAcount%26])
			response = urllib2.urlopen(request)
			soup = BeautifulSoup(response)
			info = soup.find('body')
			info = info.findAll('a')
			index = 0 # index of each retrieved url
			for urls in info:
				if (re.search(r'^<a rel="nofollow".*',str(urls))):
					# IP's associated with each domain is neglected
					if (index % 2 == 1):
						url = re.search(r'>.*<',str(urls),re.M|re.I).group()
						url = re.sub(r'>','',re.sub(r'<','',url,re.M|re.I))
						if 'http://' or 'HTTP://' not in url:
							url = re.sub(r'^','http://',url,re.M|re.I)
						urlDict[url] = 'host_file'
				else:
					self.logger.info("NO URLs available")
				index+=1		
			self.UAcount+=1

		except urllib2.HTTPError as e:
				self.logger.error("HTTPError :" + e.code)
		except urllib2.URLError as e1:
			self.logger.error("URLError :" + e1.reason)
		except Exception as e2:
			self.logger.error("Exception :" + str(e2))

