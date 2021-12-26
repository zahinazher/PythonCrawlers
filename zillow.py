#**************************************
# The script requires 1 input files 
#"*********How to run the script*****"
# Usage: "python name.py "
# You can give any name to these files. 

"""
@author: Zahin Azher
"""

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

class zillow:

  # Declare Static Variables 
  url = 'http://www.zillow.com/homes/'
  url1 = 'http://www.zillow.com'
  count_id=0

  def __init__(self):
    print "Initializing..."
    now = datetime.datetime.now()
    logging.basicConfig(filename='logs.log')
    logging.critical('Date: '+str(now))

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

  def get_house_link(self,response):
    soup = BeautifulSoup(response)
    data = soup.find('body')

    if (re.search(r'Selected Address.*?Selected Address',str(data))):
      searched = re.search(r'Selected Address.*?Selected Address',str(data)).group()
      soup1 = BeautifulSoup(searched)
      tag_a = soup1.findAll('a')
      count = 0
      for line in tag_a:
        if count == 0:
          link = re.search(r'href=".*?"',str(line)).group()
          link = re.sub(r'"',"",re.sub(r'href="',"",str(link)))
          #print link
          return link
        count +=1
      
  def get_data(self,response):
    soup = BeautifulSoup(response)
    data = soup.find('body')

    f = open('resp.txt' , 'w')

    if (re.search(r'Sold on.*?Heating Type',str(data))):
      info = re.search(r'Sold on.*?Heating Type',str(data)).group()
      f.write(str(info))
      last_sold = re.search(r'Last Sold:.*?</li>',str(info)).group()
      last_sold = re.search(r'">.*?<',str(last_sold)).group()
      last_sold = re.sub(r'">',"",re.sub(r'<',"",str(last_sold)))
      print last_sold 
      year = re.search(r' [0-9][0-9][0-9][0-9] ',str(last_sold)).group()
      year = re.sub(r'>',"",re.sub(r' ',"",str(year)))
      print "year last sold:",year
      price_sold = re.search(r'\$.*?$',str(last_sold)).group()
      #price_sold = re.sub(r' ',"",re.sub(r'$',"",str(price_sold)))
      print "price last sold:",price_sold

      #current_price = re.search(r'Sold on.*?Heating Type',str(data)).group()
      result = BeautifulSoup(info)
      result= data.findAll('span',attrs={'class':'value'})
      count1 = 0
      for line in result:
        if count1 == 1:
          price_current = re.search(r'>.*?<',str(line)).group()
          price_current = re.sub(r'<',"",re.sub(r'>',"",str(price_current)))
          print "current price:",price_current
        count1 +=1

  def main(self):
    col1 = '14515-132Nd-Ave-E'
    col2 = 'Puyallup'
    col3 = 'WA'
    uri = col1 + '%09' + col2 + '%09' + col3 +'_rb'
    url = self.url + uri
    #print url

    response = self.get_response(url,None)
    link_addr = self.get_house_link(response)
    link_addr_new = self.url1 + link_addr
    #print link_addr_new

    response = self.get_response(link_addr_new,None)
    self.get_data(response)

if __name__ == '__main__':
  if len(sys.argv)!=1 :
    print "     Incorrect input paramaters    "
    print "*********How to run the script*****"
    print "python name.py "
    sys.exit(1)

  zill = zillow()
  zill.main()
