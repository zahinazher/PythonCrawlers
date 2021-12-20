#**************************************
# The script requires 1 input files 
#"*********How to run the script*****"
# Usage: "python searchlight.py file.xlxs"
# Dependencies: BeautifulSoup, xlwt and xlrd
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
import xlwt
import xlrd
from BeautifulSoup import BeautifulSoup
#urllib2.HTTPRedirectHndler()
 
book = xlwt.Workbook(encoding="utf-8")

###############################################################################################
class Astrolight:

  # Declare Static Variables 

  def __init__(self):
    print "Initializing..."
    self.count_op_rows = 1
    self.prodcode_list = [] # used to avoid duplicates
    self.url = 'http://www.astrolighting.co.uk/products.aspx?kw='

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

  def get_product_url(self, response):
    try:
      soup = BeautifulSoup(response)

      if len(soup.findAll('div', attrs={'class':'grid-photo-box'})) > 0:
        prod_url = soup.find('div', attrs={'class':'grid-photo-box'}).find('a')['href']
        return prod_url
    except Exception as e:
      print str(e)

  def get_product(self,response, sheet1, book, prod_url):
    try:
      soup = BeautifulSoup(response)

      img_url = '' ; prod_title = '' ; prod_code = '' ; prod_desc = '' ; tech_specs = ''
      prod_cat = '' 

      # Creating a folder to put downloaded images 
      download_img = urllib.URLopener()
      dir_name = 'Astrolight'
      if not os.path.isdir(dir_name):
          os.mkdir(dir_name)
          time.sleep(1)

      if len(soup.findAll('div', attrs={'class':'reference-code'})) > 0:
        prod_code = soup.find('div', attrs={'class':'reference-code'}).text

      if len(soup.findAll('div', attrs={'class':'product-left'})) > 0:
        img_url = soup.find('div', attrs={'class':'product-left'}).find('a',id='zoom1')['href']
        img_url = re.sub(r' ','%20',re.sub(r' ','%20',str(img_url),re.I))
        img_ext = re.search(r'\.\w+$',str(img_url),re.I).group()
        # downloading product image
        #download_img.retrieve(img_url, dir_name+"/"+prod_code+img_ext)

      if len(soup.findAll('h1', attrs={'class':'productinfo'})) > 0:
        prod_title = soup.find('h1', attrs={'class':'productinfo'}).text

      if len(soup.find('div', attrs={'class':'dvlistshortdescription'})) > 0:
        prod_desc = soup.find('div', attrs={'class':'dvlistshortdescription'}).text

      if len(soup.findAll('ul', attrs={'class':'attributesSpecification'})) > 0:
        prod_tech_specs = soup.find('ul', attrs={'class':'attributesSpecification'}).findAll('li')
        for tech_sp in prod_tech_specs:
          tech_sp_text = tech_sp.text
          tech_sp_text = re.sub(r' .*$','',str(tech_sp_text),re.I)
          tech_sp_pdf =  tech_sp.find('a')['href']
          tech_sp_pdf = re.sub(r' ','%20',re.sub(r' ','%20',str(tech_sp_pdf),re.I))
          # downloading product pdf files Declaration, Datasheet and Instructions
          #download_img.retrieve(tech_sp_pdf, dir_name+"/" + prod_code + '_' + tech_sp_text + '.pdf')
          tech_specs = tech_specs + tech_sp_text + '\n' + tech_sp_pdf + '\n'


      if len(soup.findAll('div', attrs={'id':'ctl00_ContentPlaceHolder1_ctl05_dvDimensions'})) > 0:
        prod_dimension = soup.find('div', attrs={'id':'ctl00_ContentPlaceHolder1_ctl05_dvDimensions'}).text
        prod_desc = prod_desc + '\n' + prod_dimension


      if len(soup.find('ul', attrs={'class':'spec-container'}).findAll('img')) > 0:
        zone_info_all = soup.find('ul', attrs={'class':'spec-container'}).findAll('img')
        for zone_info in zone_info_all:
          zone_url = zone_info['src']
          zone_name = re.search(r'[a-zA-z0-9-]+\.gif',str(zone_url),re.I).group()
          # downloading sub images
          #download_img.retrieve(zone_url, dir_name+"/" + prod_code + '_' + zone_name)

      related_prod_codes = ''
      related_prod_titles = ''
      related_prod_img_names = ''
      if len(soup.find('ul', attrs={'class':'alternativeproducts'}).findAll('span', attrs={'class':'bluehighlight'})) > 0:
        Accessories_prod_code = soup.find('ul', attrs={'class':'alternativeproducts'}).findAll('span', attrs={'class':'bluehighlight'})

        Ac_title = soup.find('ul', attrs={'class':'alternativeproducts'}).findAll('h3')

        img_url_gen = 'http://www.astrolighting.co.uk/netalogue/zoom/'
        
        count0 = 0
        for code in Accessories_prod_code:
          rel_code = code.text
          rel_title = Ac_title[count0].text
          related_prod_codes = related_prod_codes + rel_code + '\n'
          related_prod_titles = related_prod_titles + rel_title + '\n'
          related_prod_img_names = related_prod_img_names + rel_code+'.jpg' + '\n'

          # downloading related product images from Accessories section
          #download_img.retrieve(img_url_gen+rel_code+'.jpg', dir_name+"/" + rel_code+'.jpg')
          count0 += 1

      related_prod_codes2 = ''
      related_prod_titles2 = ''
      related_prod_img_names2 = ''
      if len(soup.findAll('ul', attrs={'class':'alternativeproducts'})) > 0:
        range_prod = soup.findAll('ul', attrs={'class':'alternativeproducts'})

        range_prod_all = range_prod[len(range_prod)-2].findAll('span', attrs={'class':'bluehighlight'})

        img_url_gen = 'http://www.astrolighting.co.uk/netalogue/zoom/'

        count0 = 0
        for range_code in range_prod_all:
          range_code = range_code.text
          related_prod_codes2 = related_prod_codes2 + range_code + '\n'
          related_prod_img_names2 = related_prod_img_names2 + range_code + '.jpg' + '\n'
          # downloading related product images from Accessories section
          download_img.retrieve(img_url_gen+range_code+'.jpg', dir_name+"/" + range_code+'.jpg')
          count0 += 1

      sheet1.write(self.count_op_rows, 0, prod_url) 
      sheet1.write(self.count_op_rows, 1, 'Astrolight')
      sheet1.write(self.count_op_rows, 2, prod_code) 
      sheet1.write(self.count_op_rows, 3, 'interior lighting') 
      sheet1.write(self.count_op_rows, 4, prod_title) 
      sheet1.write(self.count_op_rows, 5, prod_desc) 
      sheet1.write(self.count_op_rows, 6, tech_specs) 
      sheet1.write(self.count_op_rows, 7, related_prod_codes)
      sheet1.write(self.count_op_rows, 8, related_prod_titles) 
      sheet1.write(self.count_op_rows, 9, related_prod_img_names) 
      sheet1.write(self.count_op_rows, 10, related_prod_codes2)
      sheet1.write(self.count_op_rows, 11, related_prod_img_names2)  
      book.save("astrolight.xlsx")
      self.count_op_rows += 1

    except Exception as e:
      print str(e)


  def call_back(self,sheet):

    global book
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0,0,'Product URL')
    sheet1.write(0,1,'Supplier')
    sheet1.write(0,2,'Product Code')
    sheet1.write(0,3,'Category')
    sheet1.write(0,4,'Title')
    sheet1.write(0,5,'Description')
    sheet1.write(0,6,'Technical Specs')
    sheet1.write(0,7,'Accessories Prodcode')
    sheet1.write(0,8,'Accessories Titles')
    sheet1.write(0,9,'Accessories Product images')
    sheet1.write(0,10,'Range prodcodes')
    sheet1.write(0,11,'Range Images')
    book.save("astrolight.xlsx")

    # Total number of rows
    num_rows = sheet.nrows
    # starting row of the input worksheet excluding row 0 that contains header
    curr_row = 1
    while curr_row < num_rows:

      prodcode = sheet.cell_value(curr_row,0)
      prodcode = re.sub(r'  $','',str(prodcode),re.I)
      prodcode = re.sub(r' $','',str(prodcode),re.I)
      prodcode = re.sub(r'^\'','',str(prodcode),re.I)
      prodcode = re.sub(r'\.0$','',str(prodcode),re.I)
      prodcode = re.sub(r' ','%20',str(prodcode),re.I)
      print prodcode

      cmd = os.popen("python crawler.py -u " +  self.url+str(prodcode) + " -f " + 'mbl.txt') 
      cmd.close()

      file1 = open('mbl.txt','r')
      response  = file1.readlines()
      response = response[0]
      # get product url
      prod_url = self.get_product_url(response)

      try:
        response = self.get_response(prod_url, None)
        # get product details
        self.get_product(response, sheet1, book, prod_url)
      except Exception as e:
        pass
      curr_row += 1

    book.save("astrolight.xlsx")

  def main(self, book):

    count = 0
    for sheet_name in book.sheet_names():
      if count == 0:
        sheet = book.sheet_by_name(sheet_name)
        self.call_back(sheet)
        
      count += 1


def main():
  filename = sys.argv[1]
  book = xlrd.open_workbook(filename)

  # AstroLight class object
  Astro = Astrolight()
  Astro.main(book)

if __name__ == '__main__':
  if len(sys.argv)!=2 :
    print "     Incorrect input paramaters     "
    print "*********How to run the script*****"
    print "python searchlight.py "
    sys.exit(1)

  main()
