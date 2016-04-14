import pymongo

"""
http://codereview.stackexchange.com/questions/64671/sharing-a-database-connection-with-multiple-modules
http://programmers.stackexchange.com/questions/200522/how-to-deal-with-database-connections-in-a-python-library-module
"""
class mongoDB(object):
    """docstring for mongoDB"""

    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = pymongo.MongoClient("mongodb://<usr>:<pwd>@ds027744.mlab.com:27744/dbdev")
        self._db_cur = self._db_connection.dbdev.chromeextn

    def query(self, query):
        return self._db_cur.find(query)

    def __del__(self):
        self._db_connection.close()



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
