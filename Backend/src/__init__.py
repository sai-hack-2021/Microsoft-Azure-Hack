import os
import pymongo
from pymongo import ReturnDocument
from functools import  wraps
from flask import request

def generatenextseqval(collectioname,db):
    """
    Function to get the new id for new doc insertion in a collection
    """
    counter = db['counter']
    try:
        val = counter.find_one_and_update(
            {'collection': collectioname},
            {'$inc': {'id': 1}},
            {'id': 1, '_id': 0},
            return_document=ReturnDocument.AFTER
        ).get('id')

        return val

    except:
        raise ("No Document Found ")


def token_required(f):
    @wraps(f)
    def  check(*args,**kwargs):
        token  = None
        if 'auth-key' in request.headers:
            token = request.headers['auth-key']

        if token == None:

            return {"message":"Token is missing"},401

        if token !='4ygdf5gthhyxx#45':
            return  {"message":"Invalid token : access Denied"}, 401

        return  f(*args,**kwargs)

    return check




def db_variables():
    """
    Function to return the environment variables
    """

    return ("azurehack.n8sw8.gcp.mongodb.net","backend","azure2020","admin","azurehack")


DB_HOST,DB_USERNAME,DB_PWD,DB_AUTH_SOURCE,DB_DATABASE = db_variables()


#initialising the connection


connection = pymongo.MongoClient("mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" %(DB_USERNAME, DB_PWD,DB_HOST,DB_AUTH_SOURCE))

db = connection[DB_DATABASE]






