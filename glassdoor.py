#**************************************
# The script requires no input file so far
#"*********How to run the script*****"
# Usage: " python yelp.com "keyword" "
# Dependencies : BeautifulSoup module
# You can give any name to these files. 

import re
import os
import csv
import sys
import urllib
import urllib2
import cookielib
import time
import random
import json
import datetime
from BeautifulSoup import BeautifulSoup
from cookielib import CookieJar

#/usr/local/lib/python2.7/dist-packages/

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

"""
v, format, t.p, t.k, userip, user-agent and action are mandatary parameter in order to use api
"""
class Glassdoor:

  op1 = "glassdoor.csv"
  if os.path.exists(op1):
    opfile = csv.writer(open(op1, 'a+'), delimiter=',')
  else:
    opfile = csv.writer(open(op1, 'w'), delimiter=',')
    opfile.writerow(["Title","Ratings","Leak Type","Location","Website","Description"])
  

  def __init__(self):

    print "Initializing..."
    self.time_now = datetime.datetime.now()
    self.count_states = 0
    self.req_id = ''
    self.url = 'http://api.glassdoor.com/api/api.htm?'

    self.partner_id =	''
    self.key =	''
    self.ip = '39.63.42.184'

    self.ua = 'Mozilla/24. (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36'
    self.curr_row = 1

    self.network_try_start = 0
    self.network_try_max = 1 # number to tries to access a particular VT url after 1st failure


  def pingingx(self):
    hostname = "google.com"
    try:
      response = os.system("ping -c 1 " + hostname)
      if response == 0:
        print "network is connected"
      else:
        print 'network is down!'
        while(response != 0):
          time.sleep(4)
          response = os.system("ping -c 1 " + hostname)
    except:
      pass

  def get_response(self,url,data):
    try:
      request = urllib2.Request(url,data)
      response = urllib2.urlopen(request)
      return response
    except urllib2.HTTPError as e:
      print "Excp in str(e.code):",str(e.code),url
      #if '400' in str(e.code):
      #  return None
    except urllib2.URLError as e1:
      print "Excp in str(e1):",str(e1),url
    except Exception as e:
      print "Excp in str(e):",str(e),url
    time.sleep(1)
    if self.network_try_start < self.network_try_max:
      self.network_try_start += 1
      self.pingingx()
      self.get_response(url,data)
    else:
      self.network_try_start = 0
      return None

  def get_states_list(self):
    f = open('states.txt' , 'rb')
    states = f.read()
    states = states.split("\n")
    while "" in states:
      states.remove("")    
    return states

  def get_states_cities_string(self):

    f = open('cities.txt' , 'rb')
    data = f.read()
    return data

  def get_cities_list(self,state_name, states_cities):
    cities_list = re.search(r'state:'+re.escape(state_name)+'.*?state:',states_cities,re.I|re.S).group()
    cities_list = re.sub(r'state:','',re.sub(r'state:'+re.escape(state_name),'',cities_list))
    cities_list = cities_list.split("\n")
    while "" in cities_list:
      cities_list.remove("")
    return cities_list

  def get_keywords_list(self,filename):
    f = open(filename, 'rb')
    data = f.readlines()
    keyword_list = []
    for name in data:
      keyword = re.sub(r'\n','',name,re.I)
      keyword = re.sub(r'\r','',keyword,re.I)
      keyword = re.sub(r'\t','',keyword,re.I)
      if keyword != '':
        keyword_list.append(keyword)
    return keyword_list

  def get_countries_list(self):
    f = open('countries.txt', 'rb')
    data = f.readlines()
    keyword_list = []
    for name in data:
      keyword = re.sub(r'\n','',name,re.I)
      keyword = re.sub(r'\r','',keyword,re.I)
      keyword = re.sub(r'\t','',keyword,re.I)
      if keyword != '':
        keyword_list.append(keyword)
    return keyword_list

  def get_data(self,data):
    title = '' ; rating = 0 ; desc = '' ; website = '' ; leak_type = 'negative' ; pros = '' ; cons = '' ; location = ''
    try:
      #print data
      try:
        website = data['website']
      except:
        pass
      try:
        rating = data['overallRating']
      except:
        pass
      try:
        featured_review = data['featuredReview']
        try:
          title = featured_review['jobTitle']
          #title = title.encode('utf-8','ignore').strip()
        except:
          try:
            title = data['ceo']
            title = title['title']
          except:
            pass
          pass
        try:
          location = featured_review['location']
        except:
          pass
        try:
          pros = featured_review['pros']
          #pros = pros.encode('utf-8','ignore').strip()
        except:
          pass
        try:   
          cons = featured_review['cons']
          #cons = cons.encode('utf-8','ignore').strip()
        except:
          pass
      except:
        pass

      try:
        if rating < 3:
          leak_type = 'Negative'
          try:
            desc = cons
          except:
            pass
        else:
          leak_type = 'Positive'
          try:
            desc = pros
          except:
            pass
      except:
        pass

      #print "title",title
      """print "rating",rating
      print "leak_type",leak_type
      print "website",website
      print "location",location
      print "pros",pros
      print "cons",cons"""
      if len(title) > 0:
        self.opfile.writerow([title,rating,leak_type,location,website,desc])

    except Exception as e:
      print "Exc in get_data:",str(e)
      pass

  def read_response(self,response):
    #result = response.read()
    status = 'OK'
    try:
      results = response
      status = results['status']
      results = results['response']
      tp = results['currentPageNumber']
      print "Current page number:",tp
      results_all = results['employers']
      #print results
      for result in results_all:
        #print result
        self.get_data(result)
        a=1
    except Exception as e:
      print "Excp in read_response:",str(e)
      pass
    return status

  def get_total_pages(self,response):
    tp = 0
    try:
      results = response
      #print results
      print "Status:",results['status']
      results = results['response']

      tp = results['totalNumberOfPages']
      print "totalNumberOfPages:",tp
    except Exception as e:
      print "Excp in get_total_pages",str(e)
      pass
    return tp
      
  def main(self):

    filename = str(sys.argv[1])
    keywords_list = self.get_keywords_list(filename)
    count_words = 0

    countries_list = self.get_countries_list()
    for keyword in keywords_list:
      if count_words >= 0:        #    countcheck  >= 0
        keyword = re.sub(r' ','+',keyword)
        print "keyword:",keyword
        count_words += 1
        count_countries = 0
        for country in countries_list:
          if count_countries >= 0 and count_countries < 200:    # countcheck >= 0
            country = re.sub(r' ','+',country)
            #country = 'California'

            link = self.url+'t.p='+self.partner_id+'&t.k='+self.key+'&userip='+self.ip+'&useragent='+\
                   '&format=json&v=1&action=employers'+'&q='+keyword+'&country='+country

            print link
            try:
              response = self.get_response(link,None)
              response = json.loads(response.read())

              status = self.read_response(response)
              if status == 'OK':
                pass
              else:
                break

              total_pages = self.get_total_pages(response)
              if int(total_pages) > 1:
              
                for cnt in range(2,total_pages+1):
                  if cnt >= 2:  # countcheck  >= 2
                    link1 = link + '&pn='+ str(cnt)
                    print link1
                    response = self.get_response(link1,None)
                    response = json.loads(response.read())
                    status = self.read_response(response)
                    if status == 'OK':
                      continue
                    else:
                      break
            except Exception as e:
              print "Exception in get response",str(e)
              pass
            #break

          count_countries += 1
          time.sleep(round(random.uniform(3, 4),2))


if __name__ == '__main__':
  if not (len(sys.argv) == 2):
    print "     Incorrect input paramaters    "
    print "*********How to run the script*****"
    print " python glassdoor.py keywords.txt " 
    sys.exit(1)
  glass = Glassdoor()
  glass.main()
