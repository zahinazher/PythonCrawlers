# Fetches suspicious urls from checkwebsitesafe

import urllib2, sys, os, re, zlib
from BeautifulSoup import BeautifulSoup

class checkwebsite:
	def __init__(self, host): 
		URL = "http://checkwebsitesafe.com/site/" + host
		headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    				'User-Agent' : 'Mozilla/5.0(compatible; MSIE 9.0; Windows NT 6.1; Trident/ 5.0; BOIE;ENUSMSNIP)',
      				'Accept-Encoding': 'gzip,deflate',
     				'Connection': 'keep-alive',
      				'Referer': 'http://checkwebsitesafe.com/',
      				'Accept-Language' : 'en-us,en;q=0.5', 
      				'Content-Type':	'application/x-www-form-urlencoded'}
		check_flag = 1
		while(check_flag == 1):
			if(self.Isnetworkon() == True):
				check_flag = 0
				try:
					request = urllib2.Request(URL, None, headers)
					response = urllib2.urlopen(request)
					self.response = response
				except:
					print "Check-Website class Exception"
					pass
			else:
				check_flag = 1

	def Isnetworkon(self):
		try:
			response=urllib2.urlopen('http://www.google.com', timeout=5)
			return True
		except urllib2.URLError as err: 
			print "except error"
			pass
			return False

	
	def getWebResult(self):
		try:
			
			arr_webresult = []
			decompressed_data=zlib.decompress(self.response.read(), 16+zlib.MAX_WBITS)
			soup = BeautifulSoup(decompressed_data)
			#print soup
			string = ''.join(re.findall(r'(<div class="domain-detail">\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)',str(soup)))
			print string
			if re.search(r'">.*?<',string):
				lst = re.findall(r'">.*?<',string)
				arr_webresult.append('Website Safety : ' + re.sub(r'">','',re.sub(r'<','',lst[0]))+'\n')
				arr_webresult.append('Google Safe Browsing : ' + re.sub(r'">','',re.sub(r'<','',lst[1]))+'\n')
				#print arr_webresult
			else:
				arr_webresult.append('NA')
			print string
			if re.search(r'<span>',string):
				lst = re.findall(r'<span>.*</span>',string)
				arr_webresult.append('WoT (Web On Trust) : ' + re.sub(r'<span>','',re.sub(r'</span>','',lst[0])))
				#print arr_webresult
			else:
				arr_webresult.append('NA')			
			return arr_webresult
		except:
			arr_webresult.append('Network Error')
			return arr_webresult
	
