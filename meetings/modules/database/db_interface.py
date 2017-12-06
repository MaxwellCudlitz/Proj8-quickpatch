
# Mongo database
# Copied from project 6
from pymongo import MongoClient
from bson.objectid import ObjectId

# module globals
MONGO_CLIENT_URL = ""
dbclient = None
db = None 
collection = None
initialized = False

def init_db(config):

    global MONGO_CLIENT_URL
    global dbclient
    global db
    global collection
    global initialized

    MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
        config.DB_USER,
        config.DB_USER_PW,
        config.DB_HOST, 
        config.DB_PORT, 
        config.DB)

    try: 
        dbclient = MongoClient(MONGO_CLIENT_URL)
        db = getattr(dbclient, config.DB)
        collection = db.dated
        initialized = True
        return True
    except:
        return False
       