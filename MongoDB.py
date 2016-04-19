import pymongo
import ConfigParser
"""
http://codereview.stackexchange.com/questions/64671/sharing-a-database-connection-with-multiple-modules
http://programmers.stackexchange.com/questions/200522/how-to-deal-with-database-connections-in-a-python-library-module
http://stackoverflow.com/questions/19379120/how-to-read-a-config-file-using-python
"""

# Read from app.config file
configParser = ConfigParser.RawConfigParser()
configFilePath = r'app.config'
configParser.read(configFilePath)

DB_URL =  configParser.get('Application-Config', 'DB_URL')
DB_USR = configParser.get('Application-Config', 'DB_USR')
DB_PASS = configParser.get('Application-Config', 'DB_PASS')

class MongoDB(object):
    """docstring for mongoDB"""

    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = pymongo.MongoClient("mongodb://"+DB_USR+":"+DB_PASS+"@"+DB_URL)
        self._db_cur = self._db_connection.dbdev.chromeextn

    def query(self, query):
        return self._db_cur.find(query)

    def update(self,query):
        return self._db_cur.udpate(query)
        
    def close(self):
        self._db_connection.close()




db = MongoDB()
try:
    cursor = db.query({})

except Exception as e:
    print "Unexpected error:", type(e), e

for doc in cursor:
    pprint.pprint(doc)

db.close()


'''
print "Connecting to database"
connection = pymongo.MongoClient("mongodb://"+DB_USR+":"+DB_PASS+"@"+DB_URL)
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
'''
