# coding: utf-8    # for special characters in python code

import re
import os
import sys
import time
import datetime
import selenium
import random
import csv
from time import strftime
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

class Leakn:

  def __init__(self):
    print "Initializing..."
    now = datetime.datetime.now()
    print "Current Time:",now
    self.url = "http://leakn.com/user/login?current=user/login"
    self.post_url = "http://leakn.com/node/add/business"

    self.username = "zahinazher"
    self.password = "123456"

    self.title_col = 0
    self.leak_type_col = 2
    self.category_col = 3
    self.location_col = 4
    self.desc_col = 5

    self.alert_try_max = 1

  def read_csv_file(self):
    with open(sys.argv[1], 'rb') as f2:
      try:
        file2_reader = csv.reader(f2, delimiter=',')
      except IOError:
        print "Error Reading csv File", f2
        sys.exit()
      title=[]
      leak_type=[]
      category = []
      location=[]
      desc = []
      for row in file2_reader:
        title.append(row[self.title_col])
        leak_type.append(row[self.leak_type_col])
        category.append(row[self.category_col])
        location.append(row[self.location_col])
        desc.append(row[self.desc_col])
      return (title,leak_type,category,location,desc)

  def login(self,driver):
    try:
      ele_un = driver.find_element_by_id("edit-name")
      ele_un = ele_un.send_keys(self.username)
      ele_pw = driver.find_element_by_id("edit-pass")
      ele_pw = ele_pw.send_keys(self.password)
      time.sleep(3)
      while True:
        try:
          print "try login"
          ele_btn = driver.find_element_by_id("edit-submit")
          ele_btn.click()
          print "success"
          break
        except Exception as e:
          print "clicking login btn attempt failed:",str(e)
          time.sleep(1)
    except Exception as e:
      print "Excp login",str(e)

  def dismiss_alert(self,driver):
    count = 0
    while count < 0:
      try:
        Alert(driver).dismiss()
        break
      except Exception as e:
        print count,"-> Excp in alert",str(e)
      time.sleep(2)
      count += 1

  def main(self):

    title = ""
    description = ""
    link_img = "file:///home/zahin/Desktop/index.jpeg"
    location = ""

    category = "Workplace Dramas"
    leak_type = "negative"

    (title_all,leak_type_all,category_all,location_all,desc_all) = self.read_csv_file()


    driver = webdriver.Firefox()

    driver.get(self.url)
    #self.dismiss_alert(driver)

    self.login(driver)
    while 'login' in str(driver.current_url):
      print "waiting to get logged in"
      time.sleep(round(random.uniform(2.5, 2.7),2))

    count = 0
    for title in title_all:
      if count == 1:# and count < 5:  # countcheck >= 1

        #leak_type = leak_type_all[count]
        #category = category_all[count]
        location = location_all[count] + ' USA'
        location = "newyork"
        description = desc_all[count]

        if len(description) < 150:
          count += 1
          continue

        print "title:",title
        print "location:",location
        #print "category:",category
        print "leak type:",leak_type
        description = re.sub(r'\n$','',re.sub(r'\n$','',description))
        description = re.sub(r'\r\r','',re.sub(r'\t\t','',description))
        description = re.sub(r'\r\r','',re.sub(r'\r\r','',description))

        if len(description) > 1000:
          description = description[:860] + '..'
        #print "Desc:",description

        try:

          time.sleep(1.4)
          print "accessing post page"
          driver.get(self.post_url)

          b_handle = driver.current_window_handle

          print "get title element"
          ele_title = driver.find_element_by_id("edit-title")
          ele_title = ele_title.send_keys(title)
          print "title pasted"

          time.sleep(0.8)
          select = Select(driver.find_element_by_id("edit-field-category-und"))
          select.select_by_visible_text(category)
          print "category selected"

          time.sleep(0.5)
          ele_zipcode = driver.find_element_by_id("search-field-coordinates-und-0")
          ele_zipcode = ele_zipcode.send_keys(location)
          print "zipcode pasted"
          time.sleep(0.8)

          if leak_type.lower() == "negative":
            ele_leaktype = driver.find_element_by_id("edit-field-leak-type-und-0") # Use 0 for -ve post and 1 for +ve post
          else:
            ele_leaktype = driver.find_element_by_id("edit-field-leak-type-und-1") # Use 0 for -ve post and 1 for +ve post
          ele_leaktype.click()
          time.sleep(0.5)
          ele_leaktype.send_keys(Keys.SPACE)
          print "leak type checked"
          time.sleep(0.9)

          ele_img_choose = driver.find_element_by_id("edit-field-photos-und-0-upload")
          ele_img_choose.send_keys(link_img)
          time.sleep(3)
          print "select image"
          ele_img_upload = driver.find_element_by_id("edit-field-photos-und-0-upload-button")
          ele_img_upload.click()
          print "image uploading"
          print "4s delay"
          time.sleep(7)

          driver.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
          driver.execute_script('document.title=oldtitle;')
          driver.execute_script('document.title')

          print "get desc element"
          while True:
            try:
              ele_textbox = driver.find_element_by_id("cke_edit-body-und-0-value")
              driver.switch_to_frame(driver.find_element_by_tag_name("iframe"));
              f_id = driver.find_element_by_tag_name("body");
              f_id.clear();
              print "trying execute iframe javascript"
              f_id.send_keys(description)
              print "description is pasted to text frame"
              time.sleep(0.7)
              break
            except Exception as e:
              print "Getting desc box handle attempt failed: trying again"
              time.sleep(1)
              pass

          time.sleep(3)
          driver.switch_to_window(b_handle)
          print "post a leak"
          ele_save_btn = driver.find_element_by_id("edit-submit")
          ele_save_btn.click()
          print "Leak successfully posted anonymously"

        except Exception as e:
          print "Exception encountered:",str(e)
        time.sleep(4)

      count += 1
    later = datetime.datetime.now()
    print "Script ended at:",later

if __name__ == '__main__':
  if len(sys.argv)!=2 :
    print "     Incorrect input paramaters    "
    print "*********How to run the script*****"
    print "python leakn.py file.csv"
    sys.exit(1)
  leakn = Leakn()
  leakn.main()
