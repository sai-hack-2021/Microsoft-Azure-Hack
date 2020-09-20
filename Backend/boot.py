import pymongo
import sys
import json


def db_variables():
    """
    Function to return the environment variables
    """

    return ("azurehack.n8sw8.gcp.mongodb.net","backend","azure2020","admin","azurehack")

print("Gettting the Database Details \n")


DB_HOST,DB_USERNAME,DB_PWD,DB_AUTH_SOURCE,DB_DATABASE = db_variables()


try:

    connection = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" %(DB_USERNAME, DB_PWD,DB_HOST,DB_AUTH_SOURCE))

    db = connection[DB_DATABASE]

    print("Database connection successfully setup")


    #making collections

    # initialising the connection

    def get_collections():

        with open("collections.json", 'r') as ff:
            return json.load(ff)


    def create_collections():
        """
       Function to create a list of collections
        """
        # deleting everything in the databse
        list_of_collections = db.list_collection_names()

        if len(list_of_collections) > 0:
            # if any existing collections are present drop them
            for col in list_of_collections:
                db.drop_collection(col)
        else:
            pass
            # this must be picked up from collection.json
        collections = get_collections()

        print(" creating collections\n")

        for collection in collections['collection_names']:
            db.create_collection(collection)

        print("Collections created successfully \n")

        # creating a counter_for_collection_names for putting incrementing
        db_collections = db.list_collection_names()
        counter = db['counter']

        print("Adding collection name in counters\n")

        for i in db_collections:
            counter.insert_one({
                'collection': i,
                'id': 0
            })


    create_collections()

except:
    print("Error in booting up \n \n ")
    print(sys.exc_info()[1])

