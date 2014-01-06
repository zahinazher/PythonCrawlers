#**************************************
# The script requires 1 input files 
#"*********How to run the script*****"
# Usage: "python searchlight.py file.xlxs"
# Dependencies: BeautifulSoup, xlwt and xlrd

##*************Copyrights**************##
## OWNER: Zahin Azher Rashid
## Dependencies: BeautifulSoup
##*************Thank You***************##

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

########################################################################################
class SearchLight:

  # Declare Static Variables 

  def __init__(self):
    print "Initializing..."
    self.count_op_rows = 1
    self.prodcode_list = [] # used to avoid duplicates
    self.url = 'http://www.searchlightelectric.com'
    self.url1 = 'http://www.searchlightelectric.com/modules/shop/stockview.asp'
    self.url2 = 'http://www.searchlightelectric.com/modules/shop/view.asp?prodcode='
    
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

  def get_prod_details(self,response, sheet1, book):

    try:
      soup = BeautifulSoup(response)

      prod_code = '' ; prod_cat = '' ; prod_range = '' ; prod_desc = '' ; prod_size = ''
      prod_watt = '' ; prod_socket = '' ; prod_img_link = '' ; prod_url = ''
 
      prod_code = soup.find('div', attrs={'class':'viewprodcode'}).text
      prod_code = re.sub(r'&nbsp;','',str(prod_code),re.I)
      prod_code = re.sub(r'Product Code:','',str(prod_code),re.I)

      prod_url = 'http://www.searchlightelectric.com/modules/shop/view.asp?prodcode=' + str(prod_code)

      # to avoid duplicates
      if prod_code in self.prodcode_list:
        return (False,'NA')
      self.prodcode_list.append(prod_code)

      if len(soup.findAll('div', attrs={'class':'viewprodcat'}))>0:
        prod_cat = soup.find('div', attrs={'class':'viewprodcat'}).text
      
      if len(soup.findAll('div', attrs={'class':'viewprodrange'})) > 0:
        prod_range = soup.find('div', attrs={'class':'viewprodrange'}).text

      if len(soup.findAll('div', attrs={'class':'viewproddescription'})) > 0:
        prod_desc = soup.find('div', attrs={'class':'viewproddescription'}).text
        prod_desc = re.search(r'</span>.*?$',str(prod_desc.encode('ascii', 'ignore')),re.I|re.S).group()
        prod_desc = re.sub(r'</span>','',str(prod_desc),re.I)

      if len(soup.findAll('div', attrs={'class':'viewprodsize'})) > 0:
        prod_size = soup.find('div', attrs={'class':'viewprodsize'}).text
        prod_size = re.sub(r'Size:','',str(prod_size.encode('ascii', 'ignore')),re.I)

      if len(soup.findAll('div', attrs={'class':'viewprodwatt'})) > 0:
        prod_watt = soup.find('div', attrs={'class':'viewprodwatt'}).text
        prod_watt = re.sub(r'Wattage:','',str(prod_watt),re.I)

      if len(soup.findAll('div', attrs={'class':'viewprodsocket'})) > 0:
        prod_socket = soup.find('div', attrs={'class':'viewprodsocket'}).text
        prod_socket = re.sub(r'Socket:','',str(prod_socket),re.I)

      if len(soup.findAll('img', attrs={'class':'imgprod'})) > 0:
        prod_img_link = soup.find('img', attrs={'class':'imgprod'})['src']
        prod_img_link = self.url + '/modules/shop/' + prod_img_link

        download_img = urllib.URLopener()
        dir_name = 'Searchlight'
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
            time.sleep(1)
        #download_img.retrieve(prod_img_link, dir_name+"/"+prod_code+ '.jpg')


      sheet1.write(self.count_op_rows, 0, prod_url) 
      sheet1.write(self.count_op_rows, 1, 'Searchlight')
      sheet1.write(self.count_op_rows, 2, prod_code) 
      sheet1.write(self.count_op_rows, 3, prod_cat) 
      sheet1.write(self.count_op_rows, 4, prod_range) 
      sheet1.write(self.count_op_rows, 5, prod_code+ '.jpg') 
      sheet1.write(self.count_op_rows, 6, prod_img_link) 
      sheet1.write(self.count_op_rows, 7, prod_size)
      sheet1.write(self.count_op_rows, 8, prod_watt) 
      sheet1.write(self.count_op_rows, 9, prod_socket) 
      sheet1.write(self.count_op_rows, 10, prod_desc)  
      book.save("searchlight.xlsx")


      assoc_list = []
      related_prod_codes = ""
      prod_associated = soup.findAll('div', attrs={'class':'assocprodimage'})
      for prod_as in prod_associated:
        assoc_link = prod_as.find('a')['href']
        r_p_c = re.search(r'=.*?$',str(assoc_link),re.I).group()
        r_p_c = re.sub(r'=','',str(r_p_c),re.I)
        related_prod_codes = related_prod_codes + r_p_c + "\n"
        assoc_link = self.url + '/modules/shop/' + assoc_link

        assoc_list.append(assoc_link)

      sheet1.write(self.count_op_rows, 11, related_prod_codes)
      self.count_op_rows += 1

      if len(assoc_list) > 0:
        return (True,assoc_list)
      else:
        return (False,'NA')

    except Exception as e:
      return (False,'NA')

  def call_back(self,sheet):

    global book
    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0,0,'Product URL')
    sheet1.write(0,1,'Supplier')
    sheet1.write(0,2,'Product Code')
    sheet1.write(0,3,'Category')
    sheet1.write(0,4,'By Finish')
    sheet1.write(0,5,'product image')
    sheet1.write(0,6,'IMAGE URL')
    sheet1.write(0,7,'Size')
    sheet1.write(0,8,'Wattage')
    sheet1.write(0,9,'Socket')
    sheet1.write(0,10,'Description')
    sheet1.write(0,11,'Associated product codes')

    # Total number of rows
    num_rows = sheet.nrows
    # starting row of the input worksheet excluding row 0 that contains header
    curr_row = 1 

    """ You can change the num_rows to limit scraping product codes"""
    while curr_row < num_rows:
      #row = sheet.row(curr_row)[0]
      #prodcode = sheet.cell_type(curr_row,0)
      prodcode = sheet.cell_value(curr_row,0)
      prodcode = re.sub(r'  $','',str(prodcode),re.I)
      prodcode = re.sub(r'^\'','',str(prodcode),re.I)
      prodcode = re.sub(r'\.0$','',str(prodcode),re.I)
      prodcode = re.sub(r' ','%20',str(prodcode),re.I)
      print prodcode

      response = self.get_response(self.url2+str(prodcode),None)

      (check,links) = self.get_prod_details(response, sheet1, book)
      if check == True:
        for link in links:
          response = self.get_response(link,None)
          self.get_prod_details(response, sheet1, book)

      curr_row += 1
    book.save("searchlight.xlsx")

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

  # SearchLight class object
  SL = SearchLight()
  SL.main(book)

if __name__ == '__main__':
  if len(sys.argv)!=2 :
    print "     Incorrect input paramaters     "
    print "*********How to run the script*****"
    print "python searchlight.py "
    sys.exit(1)

  main()


