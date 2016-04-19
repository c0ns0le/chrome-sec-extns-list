'''
Created on Dec 22, 2015

@author: rv279r

'''
import ConfigParser
import urllib2
from bs4 import BeautifulSoup
import pprint
import sys
import pymongo
import os
import datetime
import json
from bson import json_util


PROXY = 1
LIMIT_COUNT = 2
WEBSTORE_URL = "https://chrome.google.com/webstore/detail/"
DIR = os.path.dirname(os.path.realpath(__file__))

# Read from app.config file
configParser = ConfigParser.RawConfigParser()
configFilePath = r'app.config'
configParser.read(configFilePath)

PROXY_URL =  configParser.get('Application-Config', 'PROXY_URL')







'''
def read_json(data_file):
    read_path = os.path.join(DIR,data_file)
    json_data = json.load(open(read_path,'r'))

    return json_data

idlist = read_json('import.json')
'''

def return_text(attribute):
    """If tag exists, return the text else empty string."""
    if attribute != None:
        return attribute.get_text().encode('ascii', 'ignore').decode('ascii')
    else:
        return ""

def scrap_info(storeid):
    if PROXY == 1:
        proxy = urllib2.ProxyHandler({'https': PROXY_URL})
        opener = urllib2.build_opener(proxy)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        page=urllib2.urlopen(WEBSTORE_URL+storeid).read()
        soup=BeautifulSoup(page, "html.parser")

        title = soup.find("h1", {"class" : "e-f-w"})
        description = soup.find("div", {"class" : "C-b-p-j-Pb"})
        rating = soup.find("span", {"class" : "q-N-nd"}).get('aria-label')
        user_count = soup.find("span", {"class" : "e-f-ih"})
        dev_website = soup.find("a", {"class" : "e-f-y"})
        webstore_id = storeid
        chrome_extn = {'_id':webstore_id,'title':return_text(title), 'description':return_text(description),'rating':str(rating),'usercount':return_text(user_count),'website':return_text(dev_website)}

        '''
        print "Title: " + return_text(title)
        print "Description: " + return_text(description)
        print "Rating: " +  rating
        print "Users: " + return_text(user_count)
        print "Developer Website: " + return_text(dev_website)
        print "Webstore ID: " + storeid
        pprint.pprint(chrome_extn)
        '''
        return chrome_extn

    except urllib2.HTTPError, e:
        print 'We failed with error code - %s.' % e.code
        return {}

def read_data():
    print "Connecting to database"
    connection = pymongo.MongoClient("mongodb://<usr>:<pwd>@ds027744.mlab.com:27744/dbdev")
    db=connection.dbdev
    extnlist = db.chromeextn

    print "Reading Data ...\n"

    try:
        cursor = extnlist.find({})

    except Exception as e:
        print "Unexpected error:", type(e), e

    for doc in cursor:
        pprint.pprint(doc)

    connection.close()

def insert_data():
    global LIMIT_COUNT
    count = 1
    print "Connecting to database ...\n"
    connection = pymongo.MongoClient("mongodb://<usr>:<pwd>@ds027744.mlab.com:27744/dbdev")
    db=connection.dbdev
    extnlist = db.chromeextn

    print "Initiate Scraping for " , len(idlist) , "records ...\n\n"

    for storeid in idlist:
        print "Scraping Data: " + str(count) + "\n"
        extn = scrap_info(storeid);
        extn['updated']= datetime.datetime.utcnow()
        print extn
        print "\n"
        try:
            extnlist.update({"_id":storeid},{"$set":extn,"$setOnInsert": {"created": datetime.datetime.utcnow() }},upsert=True)
            #extnlist.insert_one({extn_dummy})
            print "Inserted Data: " + str(count) + "\n"
        except Exception as e:
            connection.close()
            print "Unexpected error:", type(e), e

        if count == LIMIT_COUNT:
            print "Limited Data Updated \n"
            break
        count += 1

    print count, "records updated. \n"
    connection.close()

#os.system('clear')
#insert_data()
#read_data()
'''
count =1
for storeid in idlist:
        print "\nScraping Data: " + str(count) + "\n"
        extn = scrap_info(storeid["_id"]);
        extn['updated']= str(datetime.datetime.utcnow())
        #print extn
        print json.dumps(extn, default=json_util.default)
        if count == LIMIT_COUNT:
            print "\nLimited Data Updated \n"
            break
        count += 1
'''

#print scrap_info('djflhoibgkdhkhhcedjiklpkjnoahfmg')





class ChromeSecurityExtensions():
    """docstring for ChromeSecurityExtensions"""
    def __init__(self, arg):
        super(ChromeSecurityExtensions, self).__init__()
        self.arg = arg

    def read_ids_json(data_file):
    def return_text(attribute):
    def scrap_data(storeid):
    def read_from_db():
    def write_to_db():
