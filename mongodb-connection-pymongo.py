import json
from core import logger
from pymongo import MongoClient #it is not default, you need to install the module
from bson.json_util import dumps

from core.config.mongo import settings

def get_data():

    logger.info("Getting data from mongo-db")
    db_name = "dbname"

    print("Start connection MongoDB, db={}".format(db_name))

    mongo_user = settings["mongo_user"]
    mongo_password = settings["mongo_password"]
    mongo_server = settings["mongo_server"]
    mongo_uri = f'mongodb://{mongo_user}:{mongo_password}@{mongo_server}/{db_name}'

    client = MongoClient(mongo_uri)
    db = client[db_name]
    find = db.collection.find(no_cursor_timeout=True)
    result = dumps(find)
    client.close()

    return json.loads(result)

