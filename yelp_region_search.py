#**************************************
# The script requires no input file so far
#"*********How to run the script*****"
# Usage: " python yelp.com "city + state code" "
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
import datetime
import json
from BeautifulSoup import BeautifulSoup
from cookielib import CookieJar
from crawler import *
#/usr/local/lib/python2.7/dist-packages/

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

class Yelp:

  def __init__(self):
    print "Initializing..."

    self.url_list = []   # To avoid redundancy
    self.url_list_existing = []   # To avoid redundancy in existing yelp.csv file
    self.img_counter = 1
    self.delay_pages = 0  # Delay between subsequent pages request
    self.delay_prod = 0  # Delay between subsequent pages request

    self.op_name = "yelp.csv"
    if os.path.isfile(self.op_name):
      self.url_col = 11
      with open(self.op_name, 'rb') as f:
        try:
          file_reader = csv.reader(f, delimiter=',')
        except IOError:
          print "Error Reading csv File", file_reader
          sys.exit()
        count_ = 0
        for row in file_reader: # data is read only once
          if count_ == 0:
            if 'Title' not in str(row[0]):
              self.opfile.writerow(["Title", "Category","Reviews","Rating","Address","State","City",
                     "Zip Code", "Phone","Business Info","Website","Page Link","Image Name"])
            
          self.url_list_existing.append(row[self.url_col])
          count_ += 1
      f.close()
      self.opfile = csv.writer(open(self.op_name, 'ab+'), delimiter=',')
    else:
      self.opfile = csv.writer(open(self.op_name, 'w'), delimiter=',')
      self.opfile.writerow(["Title", "Category","Reviews","Rating","Address","State","City",
                   "Zip Code", "Phone","Business Info","Website","Page Link","Image Name"])

    #self.time_now = datetime.datetime.now()
    self.count_states = 0
    self.req_id = ''
    self.url = 'http://www.yelp.com'


    self.dir_name = 'Images'
    if not os.path.isdir(self.dir_name):
        os.mkdir(self.dir_name)

  def get_response(self,url,data):
    try:
      request = urllib2.Request(url,data)
      response = urllib2.urlopen(request)
      return response
    except urllib2.HTTPError as e:
      print str(e.code)
    except urllib2.URLError as e1:
      print str(e1)
    except Exception as e:
      print str(e)
    
  def get_images_links(self,response):
    img_name = '' ; ext = '' ; img_names_str = '' 
    try:
      soup = BeautifulSoup(response)

      link_images = soup.find("div", attrs={'class':'container photo-details-base'}).find("div", {"class":"landing-section"})\
                        .find("div", { "class" : "photos" }).findAll('img')
      #print link_images
      img_names_list = []
      self.img_counter = 1
      for link_img in link_images:
        #print link_img
        photo_id = '' ; ext = ''
        try:
          link_img = link_img.get('src')
          i_name = re.search(r'[a-zA-z0-9-_]+\.[a-z]{2,5}$',str(link_img),re.I).group()
          ext = re.search(r'\.[a-z]{2,5}$',str(link_img),re.I).group()
          link_img = re.sub(re.escape(str(i_name)),'l'+str(ext),link_img,re.I)
          link_img = re.sub(r'//','',link_img,re.I)
          link_img = re.sub(r'^http:','',link_img,re.I)
          if 'http' not in link_img.lower():
            link_img = re.sub(r'^','http://',link_img,re.I)
          #print link_img
          try:
            photo_id = re.search(r'/bphoto/.*?/',link_img,re.I).group()
            photo_id = re.sub(r'/bphoto/','',photo_id,re.I)
            photo_id = re.sub(r'/','',re.sub(r'/','',photo_id,re.I))
            #print photo_id
          except:
            pass
          image_name = photo_id + '_' + str(self.img_counter) + ext
          #print "img_name",image_name

          download_img = urllib.URLopener()
          download_img.retrieve(link_img, self.dir_name + "/" + image_name)

          self.img_counter += 1
          img_names_list.append(image_name)
        except Exception as e:
          #print "Exception in retrieve",str(e)
          pass
      #img_names_str = ";".join(img_names_list)
      return img_names_list
    except Exception as e:
      #print "Exception in get_images_links:",str(e)
      return ['']

  def get_images(self,container):
    link_image_main = ''
    try:
      try:
        link_image_main = container.find("div", attrs={'class':'showcase-container'})\
                          .find("div", { "class" : "showcase-footer-links" }).findAll('a')[1].get('href')
      except:
        try:
          link_image_main = container.find("div", attrs={'class':'showcase-container'})\
                          .find("div", { "class" : "showcase-footer-links" }).findAll('a')[0].get('href')
        except:
          try:
            link_image_main = container.find("div", attrs={'class':'showcase-container'})\
                          .find("div", { "class" : "showcase-photos" })\
                          .find('a',{"class":"see-more show-all-overlay"}).get('href')
          except:
            link_image_main = container.find("div", attrs={'class':'showcase-container'})\
                          .find("div", { "class" : "showcase-photos" })\
                          .find("div",{"class":"js-photo photo photo-1"}).find('a').get('href')
      link_image_main = self.url + link_image_main
      #print link_image_main
      response = self.get_response(link_image_main,None)
      images_names_all = self.get_images_links(response)
      return images_names_all
    except Exception as e:
      #print "Exception in get_images:",str(e)
      return ['']

  def get_address(self,mapbox):
    address = '' ; address_complete = ''
    try:
      address_complete = mapbox.find("li", attrs={ "class" : "address" })
      address = address_complete.find("span", { "itemprop" : "streetAddress" }).getText()
      address = address.encode('utf-8', 'ignore').strip()
      #print address
      return address,address_complete
    except:
      return '',address_complete

  def get_city(self,address_complete):
    city = ''
    try:
      city = address_complete.find("span", { "itemprop" : "addressLocality" }).getText()
      #print city
      return city
    except:
      return ''

  def get_state(self,address_complete):
    state = ''
    try:
      state = address_complete.find("span", { "itemprop" : "addressRegion" }).getText()
      #print state
      return state
    except:
      return ''

  def get_zip_code(self,address_complete):
    zip_code = ''
    try:
      zip_code = address_complete.find("span", { "itemprop" : "postalCode" }).getText()
      #print zip_code
      return zip_code
    except:
      return ''

  def get_phone(self,mapbox):
    phone = ''
    try:
      phone = mapbox.find("span", { "itemprop" : "telephone" }).getText()
      #print phone
      return phone
    except:
      return ''

  def get_website(self,mapbox):
    website = ''
    try:
      website = mapbox.find("div", attrs={'class':'biz-website'}).find('a').getText()
      website = website.encode('utf-8', 'ignore').strip()
      #print website
      return website
    except:
      return ''

  def get_dealer(self,container):
    dealer = ''
    try:
      dealer = container.find("div", attrs={'class':'biz-page-header-left'})\
                        .find("span", { "class" : "category-str-list" }).getText()
      #print dealer
      return dealer
    except:
      return ''

  def get_reviews(self,container):
    reviews = '' ; rating = ''
    try:
      reviews = container.find("div", attrs={'class':'biz-page-header-left'}).find("div", { "class" : "rating-info clearfix" })\
                         .find("span", { "itemprop" : "reviewCount" }).getText()
      #print reviews
      try:
        rating = container.find("div", attrs={'class':'biz-page-header-left'}).find("div", { "class" : "rating-very-large" })\
                           .find("meta", { "itemprop" : "ratingValue" }).get('content')
        #print rating
        return (reviews,rating)
      except:
        pass
    except:
      return '',''

  def get_menu_link(self,data,info_dict):
    menu_link = ''
    try:
      menu_link = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'island summary'})\
                  .find("li", attrs={'class':'menu-link-block iconed-list-item'}).find('a').get('href')
      #print menu_link
      info_dict['Menu'] = menu_link
      return menu_link,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_price_range(self,data,info_dict):
    price_range = ''
    try:
      price_range = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'island summary'})\
                  .find("li", attrs={'class':'iconed-list-item'}).find('dd').getText()
      #print price_range
      info_dict['Price range'] = price_range
      return price_range,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_health(self,data,info_dict):
    health = ''
    try:
      health = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'island summary'})\
                  .find("li", attrs={'class':'iconed-list-item health-score'}).find('dd').getText()
      #print health
      info_dict['Health score'] = health
      return health,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_more_busi_info(self,data,info_dict):
    more_busi_info = ''
    try:
      more_busi_info_ = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'ywidget'})\
                  .find("div", attrs={'class':'short-def-list'}).findAll('dl')
      newline = '\n'
      total = len(more_busi_info_)
      count = 1
      for info in more_busi_info_:
        if count == total:
          newline = ''
        key = info.find('dt').getText()
        value = info.find('dd').getText()
        info_dict[key] = value
        #print key,value
        more_busi_info = more_busi_info + str(key) + ' ' + str(value) + newline
        count += 1
      #print info_dict
      return more_busi_info,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_hours(self,data,info_dict):
    hours = ''
    try:
      hours_ = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'ywidget biz-hours'}).find('tbody')\
                  .findAll('tr')
      total = len(hours_)
      count = 1
      newline = ';'
      for hr in hours_:
        if count == total:
          newline = ''
        th = hr.find('th').getText()
        hours_ = hr.find('td').getText()
        #info_dict[th] = hours_
        hours = hours + str(th) + ' ' + str(hours_) + newline
        count += 1
      info_dict.update({"Timings":hours})
      #print hours
      return hours,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_busi_info(self,data,info_dict):
    busi_info = ''
    try:
      busi_info = data.find("div", attrs={'id':'super-container'}).find("div", attrs={'class':'ywidget js-from-biz-owner'})\
                  .find('p').getText()
      busi_info = re.sub(r'&amp;','&',busi_info)
      busi_info = re.sub(r'\\u2026','...',str(busi_info))
      busi_info = re.sub(r'\u2026','...',str(busi_info))
      info_dict.update({"From Business":busi_info})
      #print busi_info
      return busi_info,info_dict
    except Exception as e:
      #print "Exception",str(e)
      return '',info_dict

  def get_data(self,response):
    link = ''
    try:
        link = response.geturl()
        soup = BeautifulSoup(response)
        data = soup.find('body')
        company_name = '' ; address = '' ; city = '' ; state = '' ; zip_code = '' ; phone = '' ; website = ''
        dealer = '' ; reviews = '' ; more_busi_info = '' ; busi_info = '' ; hours = '' ; rating = '' ;
        price_range = '' ; health = '' ; img_name = '' ; rating = ''
        info_dict = dict()
        container =  data.find("div", attrs={'class':'container'})
        company_name = container.find("div", attrs={'class':'biz-page-header-left'}).find("h1", { "itemprop" : "name" }).getText()
        company_name = company_name.encode('utf-8', 'ignore').strip()
        company_name = re.sub(r'&amp;','&',str(company_name),re.I)
        print company_name

        try:
          # Functions to get/scrape the required information
          try:
            mapbox = container.find("div", attrs={'class':'mapbox'}).find("div", attrs={'class':'mapbox-text'})
            address,address_complete = self.get_address(mapbox)
            city = self.get_city(address_complete)
            state = self.get_state(address_complete)
            zip_code = self.get_zip_code(address_complete)
            phone = self.get_phone(mapbox)
            website = self.get_website(mapbox)
          except:
            pass
          dealer = self.get_dealer(container)
          reviews,rating = self.get_reviews(container)
          menu_link,info_dict = self.get_menu_link(data,info_dict)
          price_range,info_dict = self.get_price_range(data,info_dict)
          health,info_dict = self.get_health(data,info_dict)
          more_busi_info,info_dict = self.get_more_busi_info(data,info_dict)
          hours,info_dict = self.get_hours(data,info_dict)
          busi_info,info_dict = self.get_busi_info(data,info_dict)

        except Exception as e:
          #print "Excpetion in First Try",str(e)
          pass

        img_name = self.get_images(container)

        #print info_dict
        self.opfile.writerow([company_name,dealer,reviews,rating,address,state,city,zip_code,phone,info_dict,website,link,img_name])

    except Exception as e:
      #print "Exception get_data" + str(e)
      pass

  def get_pages_links(self,data):
    try:
      tag_ul = data.find("ul", attrs={'class':'ylist ylist-bordered search-results'})
      tag_a_all = tag_ul.findAll('a', attrs={'class':'biz-name'})

      count = 0
      # Get all the 10 links on each page
      for tag_a in tag_a_all:
        if count >= 0:
          link = tag_a.get('href')
          if 'http' not in link:
            link = self.url + str(link)
            #link = "http://www.yelp.com/biz/sky-smog-test-only-torrance"
            #link = "http://www.yelp.com/biz/back-to-healthcare-chiropractic-torrance"
            #print link

            # To start off where we left off
            if str(link) in self.url_list_existing:
              count += 1
              continue
            # To ignore redundant urls if there are any
            if str(link) in self.url_list:
              count += 1
              continue
            self.url_list.append(str(link))
            response = self.get_response(link,None)
            self.get_data(response)
        time.sleep(self.delay_prod)
        count += 1

    except Exception as e:
      #print "Exception in get_pages_links",str(e)
      pass

  def get_pages_count(self,response,link):
    soup = BeautifulSoup(response)
    data = soup.find('body')
    pages_info = data.find("span", { "class" : "pagination-results-window" }).getText()
    page_info = re.findall(r"[0-9]{1,6}",pages_info,re.I|re.S)
    items_per_page = 10
    total_items_per_page = 10
    page_start_index = 0
    total_items = int(page_info[2])
    print "Total Items:",total_items
    count = 0
    # Get all the links of pages upto last page
    while (( int(total_items) + items_per_page) / total_items_per_page ) >= 1:
      if count == 0:
        #print link
        self.get_pages_links(data)
        pass
      else:
        try:
          time.sleep(self.delay_pages)
          link_new = link + "#start=" + str(page_start_index)
          #print link_new

          """response = self.get_response(link_new,None)
          soup = BeautifulSoup(response)
          self.get_pages_links(soup)"""

          cmd = os.popen('python crawler.py -u \'' +  str(link_new) + '\' -f ' + 'temp.txt') 
          cmd.close()
          file1 = open('temp.txt','r')
          response  = file1.readlines()
          response = response[0]
          data = BeautifulSoup(response)
          self.get_pages_links(data)

        except Exception as e:
          #print "Exception in get_pages_count",str(e)
          pass

      total_items_per_page += items_per_page
      page_start_index += items_per_page
      
      count += 1
  
  def main(self):

    city_name = str(sys.argv[1])

    response = self.get_response("http://www.yelp.com",None)
    soup = BeautifulSoup(response)
    #data = soup.find('body')
    r_id = re.search(r'uniqueRequestID\".*?,',str(soup),re.I).group()
    r_id = re.search(r':.*?,',str(r_id),re.I).group()
    r_id = re.search(r'\".*?\"',str(r_id),re.I).group()
    self.req_id = re.sub(r'\"','',re.sub(r'\"','',r_id,re.I))
    #print self.req_id

    word = ''
    city_name = re.sub(r' ','+',str(city_name),re.I)
    link = self.url + "/search?find_desc=" + word + "&find_loc=" + str(city_name) + "&ns=1" + "&ls=" + self.req_id
    #link = self.url + "/search?find_desc=" + word + "&find_loc=" + str(city_name) + "&ns=1"
    #print link
    try:
      response = self.get_response(link,None)
      self.get_pages_count(response,link)
      pass
    except:
      pass

if __name__ == '__main__':
  if not (len(sys.argv) == 2):
    print "     Incorrect input paramaters    "
    print "*********How to run the script*********"
    print "  python yelp.py <city + state code>" 
    print "  e.g  python yelp.py 'Torrance CA'"
    sys.exit(1)
  yelp = Yelp()
  yelp.main()
