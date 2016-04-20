import pymongo
import ConfigParser, pprint

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

class MongoDB:
    """docstring for mongoDB"""

    _db_connection = None
    _db_cur = None

    def __init__(self):
        print "Connecting to database"
        self._db_connection = pymongo.MongoClient("mongodb://"+DB_USR+":"+DB_PASS+"@"+DB_URL)
        self._db_cur = self._db_connection.dbdev.chromeextn

    def query(self, query):
        try:
             cur = self._db_cur.find(query)
             return cur
        except Exception as e:
            print "Database Error:", type(e), e
            return


    def insert(self,query,set):
        try:
            result = self._db_cur.update(query,set,upsert=True)
            return result['n']
        except Exception as e:
            print "Database Error:", type(e), e
            return

    def close(self):
        self._db_connection.close()
