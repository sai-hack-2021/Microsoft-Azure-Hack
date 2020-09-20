from functools import  wraps
from flask import request


def token_required(f):
    @wraps(f)
    def  check(*args,**kwargs):
        token  = None
        if 'auth-key' in request.headers:
            token = request.headers['auth-key']

        if token == None:

            return {"message":"Token is missing"},401

        if token !='azurehackml':
            return  {"message":"Invalid token : access Denied"}, 401


        return  f(*args,**kwargs)

    return check





