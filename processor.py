'''
Created on Dec 22, 2015

@author: rv279r
@see:
http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
http://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable-in-python

'''
import urllib2
import pprint
import os
import datetime
import json
import ConfigParser
from bs4 import BeautifulSoup
from bson import json_util
from MongoDB import MongoDB

PROXY = 0
LIMIT_COUNT = 0
WEBSTORE_URL = "https://chrome.google.com/webstore/detail/"
DIR = os.path.dirname(os.path.realpath(__file__))

# Read from app.config file
configParser = ConfigParser.RawConfigParser()
CONFIGFILEPATH = r'app.config'
configParser.read(CONFIGFILEPATH)

PROXY_URL = configParser.get('Application-Config', 'PROXY_URL')

def read_json(data_file):
    '''Reads import.json file'''
    read_path = os.path.join(*[DIR, "data", data_file])
    json_data = json.load(open(read_path, 'r'))
    return json_data

def date_handler(obj):
    '''Coverts datatime format to iso format to write to JSON'''
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def return_text(attribute):
    """If tag exists, return the text else empty string."""
    if attribute != None:
        return attribute.get_text().encode('ascii', 'ignore').decode('ascii')
    else:
        return ""

def scrap_data(storeid):
    '''Scrap information from webstore with specified store id'''
    if PROXY == 1:
        proxy = urllib2.ProxyHandler({'https': PROXY_URL})
        opener = urllib2.build_opener(proxy)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        page = urllib2.urlopen(WEBSTORE_URL+storeid).read()
        soup = BeautifulSoup(page, "html.parser")

        title = soup.find("h1", {"class" : "e-f-w"})
        description = soup.find("div", {"class" : "C-b-p-j-Pb"})
        rating = soup.find("span", {"class" : "q-N-nd"}).get('aria-label')
        user_count = soup.find("span", {"class" : "e-f-ih"})
        dev_website = soup.find("a", {"class" : "e-f-y"})
        webstore_id = storeid

        chrome_extn = {'_id':webstore_id,'title':return_text(title),
                       'description':return_text(description),
                       'rating':str(rating),
                       'usercount':return_text(user_count),
                       'website':return_text(dev_website)}
        return chrome_extn
        '''
        print "Title: " + return_text(title)
        print "Description: " + return_text(description)
        print "Rating: " +  rating
        print "Users: " + return_text(user_count)
        print "Developer Website: " + return_text(dev_website)
        print "Webstore ID: " + storeid
        pprint.pprint(chrome_extn)
        '''

    except urllib2.HTTPError, e:
        print 'Scrapping Error - %s.' % e.code
        chrome_extn = {'_id':storeid, 'title':'Not Found'}
        return chrome_extn

def read_from_db(data_file):
    '''Reads the data from database and exports to specified JSON file'''
    global LIMIT_COUNT
    count = 1
    json_docs = []

    db = MongoDB()
    cursor = db.query({})

    if cursor:
        for doc in cursor:
            pprint.pprint(doc)
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)
            if LIMIT_COUNT != 0 and count > LIMIT_COUNT:
                print "\nLimited IDs Read \n"
                break
            count += 1

    db.close()

    print count-1, "Records Found. \n"
    json_data_file = [json.loads(j_doc, object_hook=json_util.object_hook) for j_doc in json_docs]

    write_path = os.path.join(*[DIR, "data", data_file])
    with open(write_path, 'w') as outfile:
        json.dump(json_data_file, outfile, default=date_handler, indent=4, sort_keys=True)

def insert_to_db():
    '''Inserts scrapped data to database'''

    global LIMIT_COUNT
    count = 1
    idlist = read_json('import.json')

    db = MongoDB()
    print "Initiate Scraping for ", len(idlist), "records ...\n\n"

    for storeid in idlist:
        print "Scraping Data: " + str(count) + "\n"
        extn = scrap_data(storeid["_id"])
        extn['updated'] = datetime.datetime.utcnow()
        print extn
        print "Inserted", db.insert({"_id":storeid["_id"]},
                                    {"$set":extn, "$setOnInsert": {"created": datetime.datetime.utcnow()}}), "data.\n"

        if LIMIT_COUNT != 0 and count > LIMIT_COUNT:
            print "Update Limit Has Been Set \n"
            break
        count += 1

    print count-1, "records updated. \n"
    db.close()

def dryrun_scrapper():
    '''Scraps information without inserting to database'''
    idlist = read_json('import.json')
    count =1
    for storeid in idlist:
        print "\nScraping Data: " + str(count) + "\n"
        extn = scrap_data(storeid["_id"])
        extn['updated']= str(datetime.datetime.utcnow())
        #print extn
        print json.dumps(extn, default=json_util.default)

        if LIMIT_COUNT != 0 and count > LIMIT_COUNT:
            print "\nLimited IDs Scrapped \n"
            break
        count += 1

#dryrun_scrapper()
#insert_to_db()
read_from_db('export.json')
