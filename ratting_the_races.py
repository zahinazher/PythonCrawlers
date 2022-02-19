# Imports
import random
import time
import datetime
import operator
import requests
from bs4 import BeautifulSoup

from time import sleep
from seleniumrequests import PhantomJS
from seleniumrequests import Firefox
from selenium import webdriver
import os,re

# Rule 1 = Races must have 5-10 runners
# Rule 2 = Value Odds & Actual Odds must both be between 2.5 and 5
# Rule 3 = All horses must have form with 5+ runs
# Rule 4 = NAP, NB, RES ordered in terms of biggest difference between RTR 1 and 2, to smallest.
# Rule 5 = All selections must be RTR 1

# Disable Warnings
requests.packages.urllib3.disable_warnings()

# Username & Password
USERNAME = ""
PASSWORD = ""

USE_LOCAL_HTML = True
TESTING_MODE = True # LEAVE AS TRUE

# Browser Header
HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

# Set Up Session
SESSION = requests.session()
RESPONSE = requests.Response

date_ = datetime.datetime.now().strftime("%Y-%m-%d")

# Login Function
def auto_login():
    # Make the response global
    global RESPONSE

    # Login URL
    url = "https://ratingtheraces.com/wp-login.php"

    # Payload
    payload = {
        "log":USERNAME,
        "pwd":PASSWORD,
        "wp-submit": "Log in",
        "redirect_to":"https://web.ratingtheraces.com/races/latest/",
    }

    # Post the Payload to Login
    RESPONSE = SESSION.post(url, data=payload, headers=HEADERS, verify=False)
    f = open('resp.txt','wb')
    f.write(RESPONSE.text)
    global date_
    if re.search(r'([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})',RESPONSE.url):
        date_ = re.search(r'([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})',RESPONSE.url).group(1)

def get_html():
    # Check toggle
    if USE_LOCAL_HTML == False:
        # Setup User Agent
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36'
        browser = PhantomJS(executable_path="phantomjs.exe", service_log_path=os.path.devnull)

        # Setup Browser
        if TESTING_MODE == True:
            browser = webdriver.Firefox()
        else:
            browser = webdriver.PhantomJS('phantomjs.exe')

        browser.set_window_size(1400, 1000)

        # Login URL
        url = "https://ratingtheraces.com/wp-login.php?redirect_to=https://web.ratingtheraces.com/races/latest/"

        # Get Default Login Page
        browser.get(url)

        # Login
        USER_LOGIN_FIELD = browser.find_element_by_id('user_login')
        USER_LOGIN_FIELD.send_keys(USERNAME)

        USER_PASS_FIELD = browser.find_element_by_id('user_pass')
        USER_PASS_FIELD.send_keys(PASSWORD)

        LOGIN_BUTTON = browser.find_element_by_id('wp-submit')
        LOGIN_BUTTON.click()

        # Sleep for 1 seconds to let the json initiate.
        sleep(1)

        browser.save_screenshot('html_content.png')

        PAGE_SOURCE = browser.execute_script("return document.documentElement.outerHTML;").encode("utf-8")

        # Modify the page_source to make it easier to view for debugging, don't include javascript because it will just needlessly lag the page.
        PAGE_SOURCE = str(PAGE_SOURCE).replace('="/media/', '="https://web.ratingtheraces.com/media/')
        PAGE_SOURCE = str(PAGE_SOURCE).replace('="/static/css/', '="https://web.ratingtheraces.com/static/css/')
        PAGE_SOURCE = str(PAGE_SOURCE).replace('="/static/images/', '="https://web.ratingtheraces.com/static/images/')

        # Close/Quit
        browser.delete_all_cookies()
        browser.close()
        if TESTING_MODE != True:
            # Taskkill because phantonjs doesn't work correctly with .quit()
            os.system('taskkill /f /im phantomjs.exe')

        # Write response (content) to file
        HTML_FILE = open("html_content.html", 'wb')
        HTML_FILE.write(PAGE_SOURCE)
        HTML_FILE.close()

        # Process HTML with BeautifulSoup & HTML.Parser
        PROCESSED_HTML = BeautifulSoup(PAGE_SOURCE, 'html.parser')

    else:
        # Open HTML from File
        HTML_FILE = open("html_content.html", 'r').read()
        PROCESSED_HTML = BeautifulSoup(HTML_FILE, 'html.parser')
    print 'html processed'
    return PROCESSED_HTML

# Rule 1
def filter_number_of_runners(RACES):
    # Set Blank Variables
    RACE_NUMBERS = []
    NAME_LIST = []
    COUNTER = 0

    # Cycle through each race
    for COUNTER, RACE in enumerate(RACES):

        # Wipe Variable
        NAME_LIST = []

        # Find all horses in each race
        names = RACE.findAll("td", {"class": "hover name"})
        for name in names:
            name = name.findAll('a')[0]
            if "/history/horse/" in str(name):
                NAME_LIST.append(name.text)

        names = NAME_LIST

        if (len(names) >= 5 and len(names) <= 10):
            # Append just the races that fit the filters
            RACE_NUMBERS.append(COUNTER)

    return RACE_NUMBERS

# Rule 2
def filter_win_odds_and_value_odds(RACES, RACE_NUMBERS):
    # Set Blank Variables
    FILTERED_RACE_NUMBERS = []

    # For race number in race numbers
    for RACE_NUMBER in RACE_NUMBERS:

        # Setup a new race variable
        RACE = RACES[RACE_NUMBER]

        # Gather all win odds
        WIN_ODDS = [FILTERED_SELECTIONS.text for FILTERED_SELECTIONS in RACE.findAll("td", {"class": "hover win_price"})]
        REAL_ODDS = []

        # For each horses win odds in all win odds
        for WIN_ODD in WIN_ODDS:
            # Gather real odds
            try:
                NEW_WIN_ODDS = WIN_ODD.split("(")[1].strip()
            except:
                NEW_WIN_ODDS = WIN_ODD.strip()

            try:
                NEW_WIN_ODDS = NEW_WIN_ODDS.split(")")[0].strip()
            except:
                pass

            # If not blank, append to real odds
            if WIN_ODD.strip() != u"":
                REAL_ODDS.append(NEW_WIN_ODDS)

        # get the minimal value of all REAL_ODDS
        FILTERED_SELECTIONS = min(float(s) for s in REAL_ODDS)

        # Filter out all odds, which are not between filters
        if float(REAL_ODDS[0]) == FILTERED_SELECTIONS and FILTERED_SELECTIONS <= 5 and FILTERED_SELECTIONS >= 2.5:

            # Get the value odds
            value_odds = [FILTERED_SELECTIONS.text for FILTERED_SELECTIONS in RACE.findAll("td", {"class": "hover value_odds"})]

            # Get the value
            y = float(value_odds[0])

            # Filter out all odds that are not between filters
            if y <= 5 and y >= 2.5:
                FILTERED_RACE_NUMBERS.append(RACE_NUMBER)

    # Refresh main variable
    RACE_NUMBERS = FILTERED_RACE_NUMBERS

    return RACE_NUMBERS

# Rule 3
def filter_minimum_form_length(RACES, RACE_NUMBERS):
    # Set Blank Variables
    FILTERED_RACE_NUMBERS = []

    # For race number in race numbers
    for RACE_NUMBER in RACE_NUMBERS:

        # Setup a new race variable
        RACE = RACES[RACE_NUMBER]

        # Get all forms of the race
        forms = [FILTERED_SELECTIONS.text for FILTERED_SELECTIONS in RACE.findAll("td", {"class": "form hover"})]

        FILTERED_SELECTIONS = True

        # Filter out races that have runners with less than 5 races completed.
        for form in forms:
            if len(form) < 5:
                FILTERED_SELECTIONS = False

        # Create new list of races
        if FILTERED_SELECTIONS:
            FILTERED_RACE_NUMBERS.append(RACE_NUMBER)

    # Refresh main variable
    RACE_NUMBERS = FILTERED_RACE_NUMBERS

    return RACE_NUMBERS

# Rule 4
def filter_sort_biggest_rtrscore_difference(RACES, RACE_NUMBERS):

    # Set Blank Variables
    FILTERED_RACE_NUMBERS = []
    FINAL_FILTERED_RACE_NUMBERS = []

    # For race number in race numbers
    for RACE_NUMBER in RACE_NUMBERS:

        # Setup a new race variable
        RACE = RACES[RACE_NUMBER]

        # Get all rtrscores of the race
        rtrscores = [FILTERED_SELECTIONS.text for FILTERED_SELECTIONS in RACE.findAll("td", {"class": "hover rtr_score"})]

        # compute distance between rtrs
        difference = float(rtrscores[0]) - float(rtrscores[1])

        FILTERED_RACE_NUMBERS.append(difference)

    if len(FILTERED_RACE_NUMBERS) <= 3:
        FILTERED_SELECTIONS = len(FILTERED_RACE_NUMBERS)
    else:
        # else make it 3
        FILTERED_SELECTIONS = 3 # Put below if you want to filter early

    for i in range(len(FILTERED_RACE_NUMBERS)):
        # get index and value of the maximum value in differences
        index, value = max(enumerate(FILTERED_RACE_NUMBERS), key=operator.itemgetter(1))
        # append it to the last filter volume
        FINAL_FILTERED_RACE_NUMBERS.append(RACE_NUMBERS[index])
        # erase corresponding difference / set it -1 so it is not valid value anymore
        FILTERED_RACE_NUMBERS[index] = -1
        # erase corresponding filtered race/ set it -1 so it is not valid value anymore
        RACE_NUMBERS[index] = -1

    # Refresh main variable
    RACE_NUMBERS = FINAL_FILTERED_RACE_NUMBERS

    return RACE_NUMBERS

# Rule 5
def filter_choose_rtr1(RACES, RACE_NUMBERS):

    # Set Blank Variables
    SELECTIONS = []

    # For race number in race numbers
    for RACE_NUMBER in RACE_NUMBERS:

        # Setup a new race variable
        RACE = RACES[RACE_NUMBER]

        # Get Runner ID
        horse = RACE.findAll(name="tr", attrs={"class": "runner"})[0]
        id = horse["data-run-id"].strip()

        # Get Horse Name
        horse_name = horse.findAll(name="td", attrs={"class": "hover name"})[0]

        print color.BOLD + "Horse:", color.GREEN + horse_name.text.strip().replace(u"\n", " ").replace("  ", " "), color.END + color.BOLD + "ID:", color.PURPLE + id + color.END

        SELECTIONS.append(id)

    return SELECTIONS

def selecting_horse(PROCESSED_HTML):

    # Find All Race Tables
    RACES = PROCESSED_HTML.findAll("table", {"class": "race-table table table-bordered table-condensed"})

    # Rule 1
    RACE_NUMBERS = filter_number_of_runners(RACES)

    # Rule 2
    RACE_NUMBERS = filter_win_odds_and_value_odds(RACES, RACE_NUMBERS)

    # Rule 3
    RACE_NUMBERS = filter_minimum_form_length(RACES, RACE_NUMBERS)

    # Rule 4
    RACE_NUMBERS = filter_sort_biggest_rtrscore_difference(RACES, RACE_NUMBERS)

    # Rule 5
    SELECTIONS = filter_choose_rtr1(RACES, RACE_NUMBERS)

    return SELECTIONS[:3]

def marking_horses(ids):
    HEADERS['X-Requested-With'] = 'XMLHttpRequest'
    HEADERS['Referer'] = 'https://web.ratingtheraces.com/races/latest/'
    HEADERS['Host'] = 'web.ratingtheraces.com'
    HEADERS['Origin'] = 'https://web.ratingtheraces.com'
    cookie = SESSION.cookies.get_dict()
    # print cookie
    HEADERS['X-CSRFToken'] = cookie['csrftoken']
    # Create Array in correct order
    options = ['nap', 'nb', 'reserve']

    # Create Blank Variables
    option_list = []

    # Create Date
    global date_
    date = date_
    date = '2016-05-18'
    print HEADERS
    for i, id in enumerate(ids):
        option = options[i]
        option_list.append(option)
        req_time = str(time.time()).replace(".", "")
        url = "https://web.ratingtheraces.com/entries/entry/" + date + "/"
        data = {option:option,'requested_at':req_time}
        print 'options url',url
        res = SESSION.put(url, data = data, headers=HEADERS)
        print option,':',res.text
        time.sleep(3)

    cookie = SESSION.cookies.get_dict()
    HEADERS['X-CSRFToken'] = cookie['csrftoken']
    res = SESSION.get('https://web.ratingtheraces.com/entries/_enter_nap_dialog/' + date + '/', headers=HEADERS)
    print 'NAP:',res.text
    # Create payload with swapped NB and NAP to put them into the correct order.
    payload = {
        "comment":"",
        'bfsp_' + option_list[1]:"true",
        'bfsp_' + option_list[0]:"true",
        'bfsp_' + option_list[2]:"true",
    }
    cookie = SESSION.cookies.get_dict()
    HEADERS['X-CSRFToken'] = cookie['csrftoken']

    if TESTING_MODE == True:
        print color.BOLD + color.RED + "TESTING MODE ENABLED - SELECTIONS NOT SUBMITTED" + color.END
    else:
        #SESSION.post('https://web.ratingtheraces.com/entries/entry/' +  date + '/', data=payload, headers=HEADERS)
        print color.BOLD + color.RED + "TESTING MODE DISABLED BUT SELECTIONS STILL NOT SUBBMITTED ON PURPOSE" + color.END


# Main Function
def main():
    # Start Script
    print color.BOLD + color.CYAN + "Script 1 - Starting!" + color.END

    # Login
    auto_login()

    # Get HTML
    PROCESSED_HTML = get_html()

    # Get Selections
    # runnerIds = selecting_horse(PROCESSED_HTML)
    runnerIds = [u'248658', u'248659', u'248660']
    print 'Runner IDs',runnerIds
    # Submit Selections
    if len(runnerIds) == 3:
        marking_horses(runnerIds)
    else:
        print color.BOLD + color.RED + "Not enough selections." + color.END

    # End Script
    print color.BOLD + color.CYAN + "Script 1 - Ended!" + color.END

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Start main script
if __name__ == "__main__":
    main()

