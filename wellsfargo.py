#driver = webdriver.PhantomJS()
import sys
import gtk
import webkit
import warnings
import re
import os
import csv
import sys
import urllib
import urllib2
import cookielib
import time
import datetime
from optparse import OptionParser
import gobject
from BeautifulSoup import BeautifulSoup
import json
import ctypes
import requests
#from urlparse import urlparse

libgobject = ctypes.CDLL('/usr/lib/i386-linux-gnu/libgobject-2.0.so.0.3200.4')
libsoup = ctypes.CDLL('/usr/lib/i386-linux-gnu/libsoup-2.4.so.1.5.0')
libwebkit = ctypes.CDLL('/usr/lib/libwebkitgtk-1.0.so.0.13.4')

warnings.filterwarnings('ignore')
 
#****************************************
class WebView(webkit.WebView):
    def get_html(self):
        self.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
        html = self.get_main_frame().get_title()
        self.execute_script('document.title=oldtitle;')
        return html
 
#****************************************
class Crawler(gtk.Window):
  def __init__(self):
    gtk.gdk.threads_init() # suggested by Nicholas Herriot for Ubuntu Koala
    gtk.Window.__init__(self)
    self.response = None
      
  def crawl(self,url,data):
    view = WebView()
    view.open(url)
    """self.web_view.load_uri(
            'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&response_type=token&scope=%s' % (urllib.quote(app_key), urllib.quote('https://www.facebook.com/connect/login_success.html'), urllib.quote(self.scope))
            )"""
    view.connect('load-finished', self._finished_loading)
    self.add(view)
    gtk.main()
    return self.response

  def _finished_loading(self, view, frame):
    self.response = view.get_html()
    gtk.main_quit()

#****************************************
class wellsfargo:

  def __init__(self):
    print "Initializing..."
    self.username = "one2ten"
    self.password = "zzz426wer"
    self.url_main = "https://www.wellsfargo.com"
    self.url = "https://online.wellsfargo.com/signon"
    self.url_pause = 'https://online.wellsfargo.com/das/cgi-bin/session.cgi?screenid=SIGNON_PORTAL_PAUSE'
    self.url_activity = "https://online.wellsfargo.com/das/channel/accountActivityDDA?action=doSetCurrentTab&tab=find&link_name=FindTransactions&pageName=AccountActivity"
    self.op1="transaction.csv"
    self.opfile = csv.writer(open(self.op1, 'w'), delimiter=',')
    self.opfile.writerow(["Date","Description","Deposits / Credits","Withdrawals / Debits"])

  def get_auth_token(self,response):
    try:
	    soup = BeautifulSoup(response)
	    auth_token = soup.find('input', type='hidden', attrs={'name': 'authenticity_token'})
	    authtoken = auth_token['value']
	    authtoken = str(authtoken)
	    return authtoken
    except:
	    return 'NA'

  def get_response(self,URL,data):
    try:
      request = urllib2.Request(URL,data)
      response = urllib2.urlopen(request)
      return response
    except urllib2.HTTPError as e:
      print "HTTP error" , e.code
    except urllib2.URLError as e1:
      print "urllib.URLError",e1
    except Exception as e:
      print "Exception:",e

  def get_response_h(self,URL,data,headers):
    try:
      request = urllib2.Request(URL,data,headers)
      time.sleep(6)
      response = urllib2.urlopen(request)
      return response
    except urllib2.HTTPError as e:
      print "HTTP error" , e.code
    except urllib2.URLError as e1:
      print "urllib.URLError",e1
    except Exception as e:
      print "Exception:",e

  def get_url_session(self,response):
    soup = BeautifulSoup(response)
    f= open('resp1.txt' , 'wb')
    f.write(str(soup))
    body = soup.find('body')
    body = soup.find('div', attrs={'id': 'main'})
    body = soup.find('table', attrs={'id': 'menu2'})
    url_session = body.findAll('a')[1].get('href')
    return url_session

  def get_url_session_2(self,response):
    soup = BeautifulSoup(response)
    f= open('resp2.txt' , 'wb')
    f.write(str(soup))
    body = soup.find('body')
    url_session_2 = soup.find('form', attrs={'id': 'ddaShowForm'}).get('action')
    return url_session_2

  def get_url_session_3(self,response):
    soup = BeautifulSoup(response)
    body = soup.find('body')
    a_all = soup.findAll('span', attrs={'class': 'OneLinkNoTx'})
    for link in a_all:
      if re.search(r'handleInLangLinkClick',str(link),re.I):
        value = re.search(r'handleInLangLinkClick\(.*?\)',str(link),re.I).group()
        value = re.search(r'\'.*?\'',str(value),re.I).group()
        value = re.sub(r'\'','',value,re.I)
        url_session_3 = "https://online.wellsfargo.com" + value
        return url_session_3

  def get_transaction_data(self,response):
    soup = BeautifulSoup(response)
    f= open('resp3.txt' , 'wb')
    f.write(str(soup))

    body = soup.find('body')
    body = body.find('div', attrs={'id': 'transactionSectionWrapper'})
    body = body.find('table', attrs={'id': 'DDATransactionTable'})
    body = body.find('tbody')
    body = body.findAll('tr')
    for tr in body:
      date_ = tr.find('th', attrs={'class': 'rowhead'})
      if date_ is not None:
        td = tr.findAll('td')
        date_ = date_.getText()
        desc = td[0].getText()
        desc = re.sub(r'&nbsp;','',str(desc),re.I)
        desc = re.sub(r'&amp;','&',str(desc),re.I)
        dep_cred = td[1].getText()
        dep_cred = re.sub(r'&nbsp;','',str(dep_cred),re.I)
        dep_cred = re.sub(r'&amp;','&',str(dep_cred),re.I)
        wit_deb = td[2].getText()
        wit_deb = re.sub(r'&nbsp;','',str(wit_deb),re.I)
        wit_deb = re.sub(r'&amp;','&',str(wit_deb),re.I)
        self.opfile.writerow([str(date_),str(desc),str(dep_cred),str(wit_deb)])
        #print date_,";",dep_cred,";",wit_deb


  def main(self):

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler(),urllib2.HTTPRedirectHandler)
    urllib2.install_opener(opener) # globally it can be used with urlopen

    response = self.get_response(self.url_main,None)
    print "First req to main website"

    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36',
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language':'en-US,en;q=0.8',
              'Accept-Encoding':'gzip, deflate',
              'Referer':'https://www.wellsfargo.com/biz/'
              }
    details={'destination':'AccountSummary',
             'userid':self.username,
             'password':self.password,
             'screenid':'SIGNON',
             'origination':'WebCons',
             'LOB':'BIZ',
             'u_p':''
            }
    data = urllib.urlencode(details)
    response = self.get_response_h(self.url,data,headers)


    #******** Adding cookies to webkit Start**************
    #cj =  response.headers.get('Set-Cookie')
    #print "cookiejar",cj
    #session_id = requests.session()
    #set_cookie = cj

    cookiejar = libsoup.soup_cookie_jar_new()
    libsoup.soup_cookie_jar_set_accept_policy(cookiejar,0)
    for cookie in cj:
      cookieval = cookie.value
      cookiename = re.search(r' .*?=',str(cookie),re.I).group()
      cookiename = re.sub(r' ','',re.sub(r'=','',cookiename,re.I))
      print cookiename + '=' + cookieval
      libsoup.soup_cookie_jar_add_cookie(cookiejar, libsoup.soup_cookie_new(cookiename,cookieval,'https://online.wellsfargo.com','/',-1))
      session = libwebkit.webkit_get_default_session()
      libsoup.soup_session_add_feature(cookiejar,cookiejar)
    #******** Adding cookies to webkit End****************

    time.sleep(2)
    curr_url =  response.geturl()
    print curr_url

    response = self.get_response(self.url_pause,None)

    url_session = self.get_url_session(response)
    print "url_sess:",url_session

    headers = {
              'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36',
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Language':'en-US,en;q=0.8',
              'Accept-Encoding':'gzip, deflate, sdch',
              'Host':'online.wellsfargo.com',
              'Origin':'https://online.wellsfargo.com',
              'Connection':'keep-alive',
              'Cache-Control':'max-age=0',
              'Content-Type':'application/x-www-form-urlencoded',
              #'Referer':'https://online.wellsfargo.com/das/channel/accountActivityDDA?action=doSetCurrentTab&tab=find&link_name=FindTransactions&pageName=AccountActivity'
              }
    details={
            'findTabDDACommand.description':'',
            'findTabDDACommand.timeFilterValue':'11',
            'findTabDDACommand.fromDate':'05/01/14',
            'findTabDDACommand.toDate':'05/27/14',
            'findTabDDACommand.amountOrCheckFilterValue':'1',
            'findTabDDACommand.transactionTypeFilterValue':'Select One',
            'find':'Find'
            }

    data = urllib.urlencode(details)

    response = self.get_response(url_session,None)
    print response.info()
    print "status:",response.getcode()
    new_link = response.geturl()
    print "geturl:",new_link

    url_session_2 = self.get_url_session_2(response)
    print "url_session_2",url_session_2

    response = self.get_response_h(url_session_2,data,headers)
    print response.info()
    print "status:",response.getcode()
    new_link = response.geturl()
    print "geturl:",new_link

    #url_session_3 = self.get_url_session_3(response)
    #print "url_session_3:",url_session_3

    crawler = Crawler()

    response = crawler.crawl(new_link,None)

    
    self.get_transaction_data(response)

if __name__ == '__main__':
	if len(sys.argv)!=1 :
		print "     Incorrect input paramaters    "
		print "*********How to run the script*****"
		print "python wellsfargo.py"
		sys.exit(1)
	WF = wellsfargo()
	WF.main()

