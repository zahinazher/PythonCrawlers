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

##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Dependencies: BeautifulSoup
##*************Thank You***************##

###############################################################################################
class Elsteadlight:

  # Declare Static Variables 

  def __init__(self):
    print "Initializing..."
    self.count_op_rows = 0
    self.prodcode_list = [] # used to avoid duplicates
    self.url = 'http://www.elsteadlighting.com/pages/index.php?searchFieldMenu='

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

      prod_url = soup.find('div', attrs={'class':'section_link_image'}).find('a')['href']

      return 'http://www.elsteadlighting.com' + str(prod_url)
    except Exception as e:
      print str(e)

  def get_rel_product(self,response):
    try:
      soup = BeautifulSoup(response)

      if len(soup.find('div', attrs={'class':'p_p_c_left'}).findAll('h3')) > 0:
        prod_title = soup.find('div', attrs={'class':'p_p_c_left'}).find('h3').text

      if len(soup.findAll('div', attrs={'class':'product_quick_details'})) > 0:
        prod_code = soup.find('div', attrs={'class':'product_quick_details'}).text
        prod_code = re.sub(r'Stock Code:','',str(prod_code),re.I)

      if len(soup.findAll('div', attrs={'id':'gallery'})) > 0:
        prod_img = soup.find('div', attrs={'id':'gallery'}).find('a')['href']
        prod_img = re.sub(r'^\.\.','',str(prod_img),re.I)
        prod_img = re.sub(r' ','%20',re.sub(r' ','%20',str(prod_img),re.I))
        prod_img = 'http://www.elsteadlighting.com' + str(prod_img)

      return (prod_title,prod_code,prod_img)

    except Exception as e:
      return ('NA','NA','NA')


  def get_product(self,response, sheet1, book, prod_url):
    try:
      soup = BeautifulSoup(response)


      # Creating a folder to put downloaded images 
      """download_img = urllib.URLopener()
      dir_name = 'Elsteadlight'
      if not os.path.isdir(dir_name):
          os.mkdir(dir_name)
          time.sleep(1)"""

      prod_title = '' ; prod_desc = '' ; prod_brand = '' ; prod_height = '' ; prod_width = '' ; prod_finish = ''
      prod_wattage = '' ; prod_code = '' ; prod_made_in = '' ; prod_barcode = '' ; prod_weight = ''
      prod_img_name = '' ; prod_drop = '' ; prod_box_dim = '' ; prod_glass_shade = '' ; prod_ip_rating = ''

      if len(soup.findAll('div', attrs={'class':'product_quick_details'})) > 0:
        prod_code = soup.find('div', attrs={'class':'product_quick_details'}).text
        prod_code = re.sub(r'Stock Code:','',str(prod_code),re.I)
        print prod_code

      self.count_op_rows += 1
      sheet1.write(self.count_op_rows,0,prod_url)
      sheet1.write(self.count_op_rows,1,'Elstead')
      sheet1.write(self.count_op_rows,2,prod_code)

      # to avoid duplicates
      if prod_code in self.prodcode_list:
        return (False,'NA')
      self.prodcode_list.append(prod_code)

      if len(soup.find('div', attrs={'class':'p_p_c_left'}).findAll('h3')) > 0:
        prod_title = soup.find('div', attrs={'class':'p_p_c_left'}).find('h3').text
      sheet1.write(self.count_op_rows,3,prod_title)

      if len(soup.find('div', attrs={'class':'p_p_c_left'}).findAll('p')) > 0:
        prod_desc = soup.find('div', attrs={'class':'p_p_c_left'}).find('p').text
      sheet1.write(self.count_op_rows,4,prod_desc)

      if len(soup.findAll('div', attrs={'class':'spec_copy_ppcleft'})) > 0:

        prod_brand_all = soup.find('div',attrs={'class':'p_p_c_left'}).findAll('div', attrs={'class':'spec_copy_ppcleft'})
        spec_titles = soup.find('div',attrs={'class':'p_p_c_left'}).findAll('div', attrs={'class':'spec_title'})
        count2 = 0

        for spec_title in spec_titles:
          if 'Brand:' in str(spec_title):
            prod_brand = prod_brand_all[count2].text
            #print "brand",prod_brand
          if 'Fitting Height:' in str(spec_title):
            prod_height = prod_brand_all[count2].text
            #print "height",prod_height
          if 'Width / Diameter:' in str(spec_title):
            prod_width = prod_brand_all[count2].text
            #print "width",prod_width
          if 'Projection / Overall Drop:' in str(spec_title):
            prod_drop = prod_brand_all[count2].text
            #print "drop",prod_drop
          if 'Finish:' in str(spec_title):
            prod_finish = prod_brand_all[count2].text
            #print "finish",prod_finish
          if 'Max Wattage:' in str(spec_title):
            prod_wattage = prod_brand_all[count2].text
            #print "wattage",prod_wattage
          if 'IP Rating:' in str(spec_title):
            prod_ip_rating = prod_brand_all[count2].text
            #print "IP rating",prod_ip_rating
          if 'Glass/Shade:' in str(spec_title):
            prod_glass_shade = prod_brand_all[count2].text
            #print "Glass Shade",prod_glass_shade
          count2 += 1

      sheet1.write(self.count_op_rows,6,prod_brand)
      sheet1.write(self.count_op_rows,7,prod_height)
      sheet1.write(self.count_op_rows,8,prod_width)
      sheet1.write(self.count_op_rows,9,prod_drop)
      sheet1.write(self.count_op_rows,10,prod_finish)
      sheet1.write(self.count_op_rows,11,prod_wattage)
      sheet1.write(self.count_op_rows,12,prod_ip_rating)
      sheet1.write(self.count_op_rows,13,prod_glass_shade)

      if len(soup.findAll('div', attrs={'class':'product_details'})) > 0:

        prod_brand_all = soup.find('div',attrs={'class':'product_details'}).findAll('div', attrs={'class':'spec_copy'})
        spec_titles = soup.find('div',attrs={'class':'product_details'}).findAll('div', attrs={'class':'spec_title'})
        count2 = 0

        for spec_title in spec_titles:

          if 'Made In:' in str(spec_title):
            prod_made_in = prod_brand_all[count2].text
            #print "made_in",prod_made_in
          if 'Barcode:' in str(spec_title):
            prod_barcode = prod_brand_all[count2].text
            #print "barcode",prod_barcode
          if 'Fitting Weight:' in str(spec_title):
            prod_weight = prod_brand_all[count2].text
            #print "weight",prod_weight
          if 'Boxed Dimensions:' in str(spec_title):
            prod_box_dim = prod_brand_all[count2].text
            #print "dimension",prod_box_dim

          count2 += 1
      sheet1.write(self.count_op_rows,14,prod_made_in)
      sheet1.write(self.count_op_rows,15,prod_barcode)
      sheet1.write(self.count_op_rows,16,prod_weight)
      sheet1.write(self.count_op_rows,17,prod_box_dim)

      if len(soup.findAll('div', attrs={'id':'gallery'})) > 0:
        prod_img = soup.find('div', attrs={'id':'gallery'}).find('a')['href']
        prod_img = re.sub(r'^\.\.','',str(prod_img),re.I)
        prod_img = re.sub(r' ','%20',re.sub(r' ','%20',str(prod_img),re.I))
        prod_img = 'http://www.elsteadlighting.com' + str(prod_img)
        prod_img_name = re.search(r'[a-zA-z0-9-_]+\.jpg',str(prod_img),re.I).group()

        """if not os.path.isfile(dir_name+"/"+ prod_img_name):
          # downloading product image
          download_img.retrieve(prod_img, dir_name+"/"+ prod_img_name)"""
      sheet1.write(self.count_op_rows,5,prod_img_name)


      related_prod_codes = ''
      related_prod_titles = ''
      related_prod_img_names = ''
      if len(soup.findAll('div', attrs={'class':'section_link_container'})) > 0:
        rel_prod_links = soup.findAll('div', attrs={'class':'section_link_container'})
        for rel_link in rel_prod_links:
          rel_link = rel_link.find('a')['href']
          rel_link = 'http://www.elsteadlighting.com' + rel_link

          response = self.get_response(rel_link, None)
          (prod_title_rel,prod_code_rel,prod_img_rel) = self.get_rel_product(response)

          prod_img_name_rel = re.search(r'[a-zA-z0-9-_]+\.jpg',str(prod_img_rel),re.I).group()

          related_prod_codes = related_prod_codes + prod_code_rel + '\n'
          related_prod_titles = related_prod_titles + prod_title_rel + '\n'
          related_prod_img_names = related_prod_img_names + prod_img_name_rel + '\n'

          """if not os.path.isfile(dir_name + "/"+ prod_img_name_rel):
            # downloading related product image
            download_img.retrieve(prod_img_rel, dir_name + "/"+ prod_img_name_rel)"""

      sheet1.write(self.count_op_rows,18,related_prod_codes)
      sheet1.write(self.count_op_rows,19,related_prod_titles)
      sheet1.write(self.count_op_rows,20,related_prod_img_names)
      book.save("elsteadlight.xlsx")


    except Exception as e:
      print str(e)
      #sheet1.write(self.count_op_rows,0,prod_url)
      #sheet1.write(self.count_op_rows,1,'Elstead')
      #self.count_op_rows += 1

  def call_back(self,sheet):

    global book
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0,0,'Product URL')
    sheet1.write(0,1,'Supplier')
    sheet1.write(0,2,'Product Code')
    sheet1.write(0,3,'Title')
    sheet1.write(0,4,'Description')
    sheet1.write(0,5,'Product image')
    sheet1.write(0,6,'Brand')
    sheet1.write(0,7,'Fitting Height')
    sheet1.write(0,8,'Width /Diameter')
    sheet1.write(0,9,'Projection')
    sheet1.write(0,10,'Finish')
    sheet1.write(0,11,'Max Wattage')
    sheet1.write(0,12,'IP Rating')
    sheet1.write(0,13,'Glass Shade')
    sheet1.write(0,14,'Made in')
    sheet1.write(0,15,'Barcode')
    sheet1.write(0,16,'Fitting Weight')
    sheet1.write(0,17,'Boxed Dimensions')
    sheet1.write(0,18,'Related Prodcode')
    sheet1.write(0,19,'Related ProdTitles')
    sheet1.write(0,20,'Related Prodimages')
    book.save("elsteadlight.xlsx")

    # Total number of rows
    num_rows = sheet.nrows
    # starting row of the input worksheet excluding row 0 that contains header
    curr_row = 1 # start with 1
    while curr_row < num_rows:

      prod_url = sheet.cell_value(curr_row,0)

      #prodcode = re.sub(r'\.0','',str(prodcode),re.I)
      prod_url = re.sub(r' $|  $','',str(prod_url),re.I)
      prod_url = re.sub(r' ','%20',str(prod_url),re.I)
      print prod_url
      #response = self.get_response(self.url + prodcode , None)
      #prod_url = self.get_product_url(response)

      try:
        response = self.get_response(prod_url, None)
        # get product details
        self.get_product(response, sheet1, book, prod_url)
      except Exception as e:
        pass

      curr_row += 1

    book.save("elsteadlight.xlsx")


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
  Elstead = Elsteadlight()
  Elstead.main(book)

if __name__ == '__main__':
  if len(sys.argv)!=2 :
    print "     Incorrect input paramaters     "
    print "*********How to run the script*****"
    print "python searchlight.py "
    sys.exit(1)

  main()
