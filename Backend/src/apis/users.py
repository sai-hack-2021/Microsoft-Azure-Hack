from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
import sys
import random
from src.utilities.area_parser import  areas

collection_name = 'users'
collection = db[collection_name]
ticket_collection = db['ticket']


obj = areas()

list_of_areas = obj.get_areas()




"""
----------------------------------------------------------------  NAMESPACE   ------------------------------------------
"""

user_ns = Namespace("Users",description="Operations related to users")

user_model = user_ns.model('user-model', {
    'name': fields.String(required=True),
    'age': fields.Integer(required=True),
    'gender': fields.String(required=True),
    'phone-number': fields.String(required=True),
   'e-mail':fields.String(required=True),
    'password' : fields.String(required=True)

})


user_login_model = user_ns.model('user-login-model', {
'e-mail':fields.String(required=True),
    'password' : fields.String(required=True)

})

@user_ns.route('/login')
@user_ns.response(400,'Bad Request')
@user_ns.response(401,'Invalid credentials')
@user_ns.response(500,"Database Error")
class LoginUser(Resource):
    @user_ns.doc(security='ApiKeyAuth')
    @token_required
    @user_ns.expect(user_login_model)
    def post(self):
        """
        Returns the user details object if the username and password match
        """
        try:
                payload = user_ns.payload
                user = collection.find_one({"e-mail":payload['e-mail'],'password':payload['password']})

                if user:

                    user['user_id'] = user.pop('_id')

                    return user,200
                else:
                    return {"message":"invalid credentials"},401

        except:

            return {"message": "Database Error","Error":sys.exc_info()[1]}, 500




@user_ns.route('/<id>')
@user_ns.response(400,'Bad Request')
@user_ns.response(500,"Database Error")
class GetUser(Resource):
    @user_ns.doc(security='ApiKeyAuth')
    @token_required
    def get(self,id):
        """
        Returns the user details when routed through the given user_id
        """


        #logic to assign a lat long already present in the database for demo purpose  hardcoded


        try:

            value = collection.find_one({'_id':int(id)})

            active_ticket  = ticket_collection.find({'user_id':int(id)}).sort([('currentDate',-1)])


            if isinstance(active_ticket,list):
                active_ticket= active_ticket[0]
            elif isinstance(active_ticket,dict):
                pass
            else:
                active_ticket = False

            if value:

                value['user_id'] = value["_id"]
                del value['_id']

                if active_ticket:
                    #renaming the id
                    active_ticket['ticket_id'] = active_ticket['_id']
                    del active_ticket['_id']

                    value['active_ticket']  = active_ticket
                    return value, 200
                else:
                    return value, 200

            else:
                return {"message":"User not Found"},200
        except:

            return  {"message":"Database Error","Error":sys.exc_info()[1]},500



@user_ns.route('/add')
@user_ns.response(400,'Bad Request')
@user_ns.response(200,'Successful Insertion')
@user_ns.response(500,"Database Error")
class putUser(Resource):
    @user_ns.doc(security='ApiKeyAuth')
    @user_ns.expect(user_model)
    @token_required
    def post(self):
        """
        Returns True after successful user addition in the database
        """
        try:

            val = random.randint(0,len(list_of_areas)-1)

            area_val = list_of_areas[val]

            payload = user_ns.payload

            payload.update(area_val)

            payload['_id'] = generatenextseqval(collection_name,db)

            collection.insert_one(payload)

            return  True,200
        except:

            return {"message": "Database Error"},500



@user_ns.route('/area/stats/<id>')
@user_ns.response(400,'Bad Request')
@user_ns.response(401,"User not found")
@user_ns.response(500,"Database Error")
class getUserStats(Resource):
    def get(self,id):

        # logic to fetch the user area details and get its statistics and send them

        try:
            user = collection.find_one({'_id': int(id)},{"area_id":1,"_id":1})

            if isinstance(user,dict):
                return obj.get_stats(str(user['area_id'])),200
            else:
                return {"message":"User does not exist"},200


        except:

            return {"message":"Database Error","Error":sys.exc_info()[1]},500




