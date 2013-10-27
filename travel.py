#**************************************
# The script requires no input file so far
#"*********How to run the script*****"
# Copyrights: ZAHIN
# Dependencies : BeautifulSoup module
# You can give any name to these files. 

# Some modules have been deliberatrly removed 
# due to Copyright reasons
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
#/usr/local/lib/python2.7/dist-packages/

class travel:

  # Declare Static Variables 
  url = 'anonymous.com'
  count_city = 1
  count_hotel = 1
  count_image = 0

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
      logging.warning('HTTP error:' + str(e.code))
    except urllib2.URLError as e1:
      logging.warning('URLError:' + str(e1))
    except Exception as e:
      logging.warning(str(e))

  def get_country_link(self,response,name_country):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')
      tag_li = data.findAll('li')

      for line_li in tag_li:
        if re.search(re.escape(name_country),str(line_li),re.I):
          tag_a = line_li.find('a')
          if re.search(r"href.*?>",str(tag_a),re.I):
            link = re.search(r"href.*?>",str(tag_a),re.I).group()
            link = re.sub(r"href=","",re.sub(r">","",str(link),re.I))
            link = re.sub(r"\"","",str(link),re.I)
            #print link
            return link
    except Exception as e:
      logging.warning("Fetching Country link failed: "+str(name_country))

  def get_city_link(self,response,name_city,name_country):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')

      data_ = re.search("<h2>.*?<div>.*?<div",str(data),re.I|re.S).group()
      data = BeautifulSoup(data_)

      tag_ul = data.findAll('ul')

      for line_ul in tag_ul:
        if self.count_city != 1:
          tag_li = line_ul.find('li')

          if re.search(re.escape(name_city),str(tag_li),re.I):
            tag_a = line_ul.find('a')
            if re.search(r"href.*?>",str(tag_a),re.I):
              link = re.search(r"href.*?>",str(tag_a),re.I).group()
              link = re.sub(r"href=","",re.sub(r">","",str(link),re.I))
              link = re.sub(r"\"","",str(link),re.I)
              #print link
              return link
        self.count_city += 1
    except Exception as e:
      logging.warning("Fetching City link failed: "+str(name_city))

  def get_state_link_of_us(self,response,name_city,name_country):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')

      tag_ul = data.findAll('ul')

      for line_ul in tag_ul:
        if self.count_city != 1:
          tag_li = line_ul.find('li')

          if re.search(re.escape(name_city),str(tag_li),re.I):
            tag_a = line_ul.find('a')
            if re.search(r"href.*?>",str(tag_a),re.I):
              link = re.search(r"href.*?>",str(tag_a),re.I).group()
              link = re.sub(r"href=","",re.sub(r">","",str(link),re.I))
              link = re.sub(r"\"","",str(link),re.I)
              #print link
              return link
        self.count_city += 1
    except Exception as e:
      logging.warning("Fetching State link failed: "+str(name_city))

  def get_city_link_of_us(self,response,name_city,name_country):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')
      f1=open('resp.txt' , 'w')

      link_list = []
      city_name_list = []

      data_ = re.search("<h2>.*?<div>.*?<div",str(data),re.I|re.S).group()
      data = BeautifulSoup(data_)
      tag_ul = data.findAll('ul')
      f1.write(str(tag_ul))
      for line_ul in tag_ul:
        tag_li = line_ul.find('li')
        if re.search(r"href.*?>",str(tag_li),re.I):
          link_name = re.search(r"href.*?>.*<",str(tag_li),re.I).group()

          link = re.search(r"http.*?\"",str(link_name),re.I).group()
          link = re.sub(r"\"","",str(link),re.I|re.S)
          link_list.append(link)

          city_name = re.search(r">.*?,",str(link_name),re.I).group()
          city_name = re.sub(r">","",str(city_name),re.I|re.S)
          city_name = re.sub(r",","",str(city_name),re.I|re.S)
          city_name_check = city_name
          city_name_list.append(city_name)

      return (link_list,city_name_list)
    except Exception as e:
      logging.warning("Fetching City link failed: "+str(name_city))

  def get_hotel_link(self,response,name_city,name_country):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')
      f1=open('resp.txt' , 'w')

      link_list = []
      hotel_name_list = []

      tag_a = data.findAll('a')

      for line_a in tag_a:
        look = "class=\"hotelpic"
        if look in str(line_a):
          if re.search(r"href.*?>",str(line_a),re.I):
            link = re.search(r"href.*?>",str(line_a),re.I).group()
            link = re.sub(r"href=","",re.sub(r">","",str(link),re.I))
            link = re.sub(r"\"","",str(link),re.I)
            link_list.append(link)

      result= data.findAll('div',attrs={'class':'new-listing-heading'})
      for tag_h in result:
          a=str(tag_h)
          if re.search(r"<h3>.*?</h3>",str(a),re.I|re.S):
            hotel_name = re.search(r"<h3>.*?</h3>",str(a),re.I|re.S).group()
            hotel_name = re.sub(r"<h3>","",re.sub(r'</h3>',"",str(hotel_name),re.I))
            #print hotel_name
            hotel_name_list.append(hotel_name)

      return (link_list,hotel_name_list)
    except Exception as e:
      logging.warning("Fetching Hotel links failed of city "+str(name_city))

    self.count_hotel += 1

  def get_hotel_info(self,response,name_country,name_city,hotel_name):
    try:
      soup = BeautifulSoup(response)
      data = soup.find('body')

      dir_name_hotel = 'hotels'
      if not os.path.isdir(dir_name_hotel):
        os.mkdir(dir_name_hotel)

      hotel_name_wid_spaces = hotel_name
      hotel_name = re.sub(r' ',"",re.sub(r">","",str(hotel_name),re.I))
      #print hotel_name

      op_file_name = "hotels/" + hotel_name + ".txt"
      f = open(op_file_name , 'w')
      f.write("{{Country Name}}\n" + name_country + "\n")
      f.write("{{City Name}}\n" + name_city + "\n")

      f.write("{{Hotel Name}}\n"+hotel_name_wid_spaces+"\n")

      if re.search(r"Hotel Description.*?</div>",str(data),re.I|re.S): 
        hotel_desc = re.search(r"Hotel Description.*?</div>",str(data),re.I|re.S).group()
        hotel_desc = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_desc),re.I|re.S))
        #hotel_desc = re.sub(r"\n","",str(hotel_desc),re.I|re.S)
        hotel_desc = re.sub(r"Hotel Description","{{Hotel Description}}",str(hotel_desc),re.I|re.S)
        hotel_desc = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_desc),re.I|re.S))
        hotel_desc = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_desc),re.I|re.S))
        hotel_desc = re.sub(r"<br />","\n",str(hotel_desc),re.I|re.S)
        hotel_desc = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_desc),re.I|re.S))
        hotel_desc = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_desc),re.I|re.S))
        f.write("\n"+hotel_desc)
        #print hotel_desc

      if re.search(r"Hotel Amenities.*?</div>",str(data),re.I|re.S): 
        hotel_amenities = re.search(r"Hotel Amenities.*?</div>",str(data),re.I|re.S).group()
        hotel_amenities = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_amenities),re.I|re.S))
        hotel_amenities = BeautifulSoup(hotel_amenities)
        tag_li = hotel_amenities.findAll('li')
        if tag_li is not None:
          amenities = "\n{{Hotel Amenities}}\n"
          for line_li in tag_li:
            line_li = re.sub(r"<li>","",re.sub(r"</li>","",str(line_li),re.I))
            line_li = re.sub(r"&#x0D","",re.sub(r"&#x0D;","",str(line_li),re.I))
            line_li = re.sub(r"&#x09","",re.sub(r"&#x09;","",str(line_li),re.I))
            amenities = amenities + str(line_li) + "\n"
          f.write(amenities)
          #print amenities

      if re.search(r"Hotel Information.*?</div>",str(data),re.I|re.S):
        hotel_information = re.search(r"Hotel Information.*?</div>",str(data),re.I|re.S).group()
        hotel_information = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_information),re.I|re.S))
        hotel_information = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_information),re.I|re.S))
        hotel_information = re.sub(r"Hotel Information","{{Hotel Information}}",str(hotel_information),re.I|re.S)
        hotel_information = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_information),re.I|re.S))
        hotel_information = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_information),re.I|re.S))
        f.write(hotel_information)
        #print hotel_information

      if re.search(r"Hotel Area Information.*?</div>",str(data),re.I|re.S):
        hotel_area_information = re.search(r"Hotel Area Information.*?</div>",str(data),re.I|re.S).group()
        hotel_area_information = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_area_information),re.I|re.S))
        hotel_area_information = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_area_information),re.I|re.S))
        hotel_area_information = re.sub(r"<b>","",re.sub(r"</b>","",str(hotel_area_information),re.I|re.S))
        hotel_area_information = re.sub(r"<br />","\n",str(hotel_area_information),re.I|re.S)
        hotel_area_information = re.sub(r"Hotel Area Information","{{Hotel Area Information}}",str(hotel_area_information),re.I|re.S)
        hotel_area_information = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_area_information),re.I|re.S))
        hotel_area_information = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_area_information),re.I|re.S))
        f.write("\n"+hotel_area_information)
        #print hotel_area_information

      if re.search(r"Hotel Room Information.*?</div>",str(data),re.I|re.S):
        hotel_room_information = re.search(r"Hotel Room Information.*?</div>",str(data),re.I|re.S).group()
        hotel_room_information = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_room_information),re.I|re.S))
        #hotel_room_information = re.sub(r"\n","",str(hotel_room_information),re.I|re.S)
        hotel_room_information = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_room_information),re.I|re.S))
        hotel_room_information = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_room_information),re.I|re.S))
        hotel_room_information = re.sub(r"<br />","\n",str(hotel_room_information),re.I|re.S)
        hotel_room_information = re.sub(r"<li>","",re.sub(r"</li>","",str(hotel_room_information),re.I|re.S))
        hotel_room_information = re.sub(r"<ul>","",re.sub(r"</ul>","",str(hotel_room_information),re.I|re.S))
        hotel_room_information = re.sub(r"Hotel Room Information","{{Hotel Room Information}}",str(hotel_room_information),re.I|re.S)
        hotel_room_information = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_room_information),re.I|re.S))
        hotel_room_information = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_room_information),re.I|re.S))
        f.write("\n"+hotel_room_information)
        #print hotel_room_information

      if re.search(r"Hotel Policy.*?</div>",str(data),re.I|re.S):
        hotel_policy = re.search(r"Hotel Policy.*?</div>",str(data),re.I|re.S).group()
        hotel_policy = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_policy),re.I|re.S))
        #hotel_policy = re.sub(r"\n","",str(hotel_policy),re.I|re.S)
        hotel_policy = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_policy),re.I|re.S))
        hotel_policy = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_policy),re.I|re.S))
        hotel_policy = re.sub(r"<br />","\n",str(hotel_policy),re.I|re.S)
        hotel_policy = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_policy),re.I|re.S))
        hotel_policy = re.sub(r"Hotel Policy","{{Hotel Policy}}",str(hotel_policy),re.I|re.S)
        f.write("\n"+hotel_policy)
        #print hotel_policy

      if re.search(r"Hotel Check In/Check Out Policy.*?</div>",str(data),re.I|re.S):
        hotel_inout_policy = re.search(r"Hotel Check In/Check Out Policy.*?</div>",str(data),re.I|re.S).group()
        hotel_inout_policy = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_inout_policy),re.I|re.S))
        #hotel_inout_policy = re.sub(r"\n","",str(hotel_inout_policy),re.I|re.S)
        hotel_inout_policy = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_inout_policy),re.I|re.S))
        hotel_inout_policy = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_inout_policy),re.I|re.S))
        hotel_inout_policy = re.sub(r"<br />","\n",str(hotel_inout_policy),re.I|re.S)
        hotel_inout_policy = re.sub(r"Hotel Check In/Check Out Policy","{{Hotel Check In/Check Out Policy}}",str(hotel_inout_policy),re.I|re.S)
        hotel_inout_policy = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_inout_policy),re.I|re.S))
        hotel_inout_policy = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_inout_policy),re.I|re.S))
        f.write("\n"+hotel_inout_policy)
        #print hotel_inout_policy

      if re.search(r"Hotel Check In Instructions.*?</div>",str(data),re.I|re.S):
        hotel_inout_inst = re.search(r"Hotel Check In Instructions.*?</div>",str(data),re.I|re.S).group()
        hotel_inout_inst = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_inout_inst),re.I|re.S))
        #hotel_inout_inst = re.sub(r"\n","",str(hotel_inout_inst),re.I|re.S)
        hotel_inout_inst = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r"<br />","\n",str(hotel_inout_inst),re.I|re.S)
        hotel_inout_inst = re.sub(r"<ul>","",re.sub(r"</ul>","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r"<li>","",re.sub(r"</li>","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_inout_inst),re.I|re.S))
        hotel_inout_inst = re.sub(r"Hotel Check In Instructions","{{Hotel Check In Instructions}}",str(hotel_inout_inst),re.I|re.S)
        f.write("\n"+hotel_inout_inst)
        #print hotel_inout_inst

      if re.search(r"Hotel Miscellaneous.*?</div>",str(data),re.I|re.S):
        hotel_miscell = re.search(r"Hotel Miscellaneous.*?</div>",str(data),re.I|re.S).group()
        hotel_miscell = re.sub(r"</h.?>","",re.sub(r"</div>","",str(hotel_miscell),re.I|re.S))
        #hotel_miscell = re.sub(r"\n","",str(hotel_miscell),re.I|re.S)
        hotel_miscell = re.sub(r"<p>","",re.sub(r"</p>","",str(hotel_miscell),re.I|re.S))
        hotel_miscell = re.sub(r"<b>","\n",re.sub(r"</b>","",str(hotel_miscell),re.I|re.S))
        hotel_miscell = re.sub(r"<br />","\n",str(hotel_miscell),re.I|re.S)
        hotel_miscell = re.sub(r"Hotel Miscellaneous","{{Hotel Miscellaneous}}",str(hotel_miscell),re.I|re.S)
        hotel_miscell = re.sub(r'&#x0D',"",re.sub(r"&#x0D;","",str(hotel_miscell),re.I|re.S))
        hotel_miscell = re.sub(r'&#x09',"",re.sub(r"&#x09;","",str(hotel_miscell),re.I|re.S))
        f.write(hotel_miscell)
        #print hotel_miscell

      try:
        result = data.find('ul',attrs={'class':'thumbs'})
        if result is not None:
          tag_img = result.findAll('a')
          download_img = urllib.URLopener()
          current_dir = os.getcwd()
          
          dir_name = 'images'
          if not os.path.isdir(dir_name):
              os.mkdir(dir_name)
              #os.chdir(dir_name)
          time.sleep(1)

          for image in tag_img:
            if re.search(r"href=\".*?><",str(image),re.I|re.S):
              link_img = re.search(r"href=\".*?><",str(image),re.I|re.S).group()
              link_img = re.search(r"title=\".*?\"",str(link_img),re.I|re.S).group()
              link_img = re.sub(r"\"","",re.sub(r"title=","",str(link_img),re.I))
              http = re.search(r"http://.*/",str(link_img),re.I).group()
              image_name = re.sub(re.escape(http),"",str(link_img),re.I)
              image_name = hotel_name + "_" + image_name
              download_img.retrieve(link_img,dir_name+"/"+image_name)
              #print image_name

        else:
          logging.warning("No pictures of Hotel "+str(hotel_name))
      except Exception as e:
         logging.warning("No pictures of Hotel "+str(hotel_name))
    except Exception as e:
      logging.warning("Fetching Hotel information failed, city:"+str(name_city))
 
  def main(self):
    name_country = sys.argv[1]
    name_city = sys.argv[2]

    try:

      if name_country.lower() in "united states of america":
        link_country = 'anonymous.com'
        print "link_country:",link_country
        try:
          response = self.get_response(link_country,None)
          link_state = self.get_state_link_of_us(response,name_city,name_country)
          print "link_state:",link_state
          response = self.get_response(link_state,None)
          (link_city_list,city_name_list) = self.get_city_link_of_us(response,name_city,name_country)

          link_city_list = sorted(set(link_city_list))
          city_name_list = sorted(set(city_name_list))

          for link_city in link_city_list:
            print "link_city:",link_city
          sys.exit(0)
        except Exception as e:
          logging.warning("Error City link:"+str(e))

      else:
        response = self.get_response(self.url,None)
        link_country = self.get_country_link(response,name_country)
        print "link_country:",link_country

        try:
          response = self.get_response(link_country,None)
          link_city = self.get_city_link(response,name_city,name_country)
          print "link_city:",link_city

        except Exception as e:
          logging.warning("Error City link:"+str(e))

        try:
          response = self.get_response(link_city,None)
          (link_hotel_list,hotel_name_list) = self.get_hotel_link(response,name_city,name_country)

          if len(link_hotel_list) > 0:
            count_hot = 0
            print "Total Number of Hotels in city",name_city,"is/are",len(link_hotel_list)
            for link_hotel in link_hotel_list:
              print "link_hotel:",link_hotel
              response = self.get_response(link_hotel,None)
              self.get_hotel_info(response,name_country,name_city,hotel_name_list[count_hot])
              count_hot += 1

        except Exception as e:
          logging.warning("Error Hotel link:"+str(e))
    except Exception as e:
      logging.warning("Error Country link:"+str(e))

if __name__ == '__main__':
  if len(sys.argv)!=3 :
    print "     Incorrect input paramaters    "
    print "*********How to run the script*****"
    print "python test.py \"countryname\" \"cityname\"" 
    sys.exit(1)
  travel_obj = travel()
  travel_obj.main()

