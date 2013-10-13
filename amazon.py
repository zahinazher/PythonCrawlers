#**************************************
# The script requires 1 input files 
#"*********How to run the script*****"
# Usage: "python test1.py <upc.txt>"
# You can give any name to these files. 


import re
import os
import csv
import sys
import urllib
import urllib2
import cookielib
import time
import datetime
import logging
from BeautifulSoup import BeautifulSoup
#urllib2.HTTPRedirectHndler()
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler())
urllib2.install_opener(opener) # globally it can be used with urlopen

class amazon:

	# Declare Static Variables 
	url = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
	count_id=0

	def __init__(self):
		print "Initializing..."
		now = datetime.datetime.now()
		logging.basicConfig(filename='logs.log')
		logging.critical('Date: '+str(now))

	def get_ids(self):
		with open(sys.argv[1], 'rb') as f:
			try:
				file2_reader = csv.reader(f, delimiter=',')
			except IOError:
				print "Error Reading csv File", f
				sys.exit()
			ids = []
			for row in file2_reader:
				ids.append(row[0])
                       	return (ids)

	def get_response(self,URL,data):
		try:
			request = urllib2.Request(URL,data)
			response = urllib2.urlopen(request)
			return response
		except urllib2.HTTPError as e:
			#print "HTTP error" , e.code
			logging.warning('HTTP error:' + str(e.code))
			#pass
		except urllib2.URLError as e1:
			#print "urllib.URLError",e1
			logging.warning('URLError:' + str(e1))
			#pass
			"""while (self.check_connectivity() == False):
				pass"""
		except Exception as e:
			print "Exception:",e
			logging.warning(str(e))

	def get_product(self,response):
		soup = BeautifulSoup(response)
		data = soup.find('body')
		#f=open("resp.txt" , 'w')
		#f.write(str(data))
		
		try:
			dp = soup.find('div',attrs={'id':'result_0'})
			if (re.search(r'name=.*?>',str(dp))):
				dp = re.search(r'name=.*?>',str(dp)).group()
				dp = re.sub(r'">','',re.sub(r'name=.','',str(dp),re.I))
				#print dp

			title = soup.find('div',attrs={'class':'productTitle'})
			title = title.find('a')
			href=title.get('href')
			#print href

			if (re.search(r'<.*?<',str(title))):
				title = re.search(r'>.*?<',str(title)).group()
				title = re.sub(r'<','',re.sub(r'>','',str(title),re.I))
				title = re.sub(r'^ ','',re.sub(r'$ ','',str(title),re.I))
				#print title
		
			starsAndPrime = soup.find('div',attrs={'class':'starsAndPrime'})
			if (re.search(r'class=".*?getargs=.*?>',str(starsAndPrime))):
				ref_id = re.search(r'class=".*?getargs=.*?>',str(starsAndPrime)).group()
				ref_id = re.search(r'ref=.*?getargs',str(ref_id)).group()
				ref_id = re.search(r'".*?"',str(ref_id)).group()
				ref_id = re.sub(r' ','',re.sub(r'"','',str(ref_id),re.I))
				#print ref_id

			if (re.search(r'getargs.*?>',str(starsAndPrime))):
				getargs = re.search(r'getargs.*?>',str(starsAndPrime)).group()
				if (re.search(r'qid":".*?"',str(getargs))):
					q_id = re.search(r'qid":".*?"',str(getargs)).group()
					q_id = re.sub(r'"','',re.sub(r'qid":"','',str(q_id),re.I))
					#print q_id
				if (re.search(r'sr":".*?"',str(getargs))):
					sr_id = re.search(r'sr":".*?"',str(getargs)).group()
					sr_id = re.sub(r'"','',re.sub(r'sr":"','',str(sr_id),re.I))
					#print sr_id

			return (dp,title,href,ref_id,q_id,sr_id)
			#return dp
		except Exception as e:
			logging.warning('Getting product post data failed')

	def get_product_details(self,response):
		soup = BeautifulSoup(response)
		data = soup.find('body')
		f=open("resp1.txt" , 'w')
		f.write(str(data))

		try:
			if (re.search(r'Product Details.*?Customers Who Viewed',str(data),re.I|re.M|re.DOTALL)):
				p_det = re.search(r'Product Details.*?Customers Who Viewed',str(data),re.I|re.M|re.DOTALL).group()
				if (re.search(r'ASIN.*?</li>',str(p_det))):
					asin = re.search(r'ASIN.*?</li>',str(p_det)).group()
					asin = re.search(r'>.*?<',str(asin)).group()
					asin = re.sub(r'<','',re.sub(r'>','',str(asin),re.I))
					#print asin
				if (re.search(r'Item model number.*?</li>',str(p_det))):
					item_model_no = re.search(r'Item model number.*?</li>',str(p_det)).group()
					item_model_no = re.search(r'>.*?<',str(item_model_no)).group()
					item_model_no = re.sub(r' ','',re.sub(r'<','',re.sub(r'>','',str(item_model_no),re.I)))
					#print item_model_no
				
				return (asin,item_model_no)	
		except Exception as e:
			logging.warning('Getting product Details failed')


	def main(self):
		upc_list=self.get_ids()
		#print upc_list
		op1="output.csv" 
		opfile1 = csv.writer(open(op1, 'w'), delimiter=',')
		opfile1.writerow(["UPC","ASIN","dp"])
		for upc in upc_list:
			url1 = self.url + upc

			if self.count_id < 5:
				#print url1
				try:
					response = self.get_response(url1,None)
					(dp,title,href,ref_id,q_id,sr_id) = self.get_product(response)
					#dp = self.get_product(response)

					#print "dp:"+dp+",prod_title:"+title
					#print "href:"+href+",ref_id:"+ref_id
					#print "q_id:"+q_id+",sr_id:"+sr_id

					url2 = href+"/ref="+ref_id+"?ie=UTF8&qid="+q_id+"&sr="+sr_id+"&keywords="+upc
					#print url2
					
					response = self.get_response(url2,None)
					(asin,item_model_no) = self.get_product_details(response)
					print "ASIN: "+asin+" ,item_model_no: "+item_model_no

					opfile1.writerow([upc,dp])

				except Exception as e:
					logging.warning('No response: ' + str(upc))
					
			self.count_id+=1
			

if __name__ == '__main__':
	if len(sys.argv)!=2 :
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python test1.py <upc.txt>"
		sys.exit(1)
	amaz = amazon()
	amaz.main()

