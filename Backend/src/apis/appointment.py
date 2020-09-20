from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
import sys
from datetime import datetime as dt
from src.utilities.area_parser import areas
import random
obj = areas()



ticket_coll = db['ticket']
user_col = db['users']

appoint_ns = Namespace("appointment",description="Operations related to Appointments")

appoint = appoint_ns.model("put_appoint_model",{
    "ticket_id":fields.Integer(required=True),
    "type": fields.String(required=True),
    "date": fields.String(),
    "time_slot":fields.String()
})

get_appoint = appoint_ns.model("get_appointment",{"ticket_id":fields.Integer(required=True)})

change_appoint = appoint_ns.model("change_appoint",{"ticket_id":fields.Integer(required=True),
                                                    "type":fields.String(required=True),
                                                    "time_slot":fields.Boolean(),
                                                    "date": fields.String()
                                                    })

list_appoint = appoint_ns.model("get_list",{"type":fields.String(required=True),"ticket_id":fields.Integer(required=True)})

appoint_types = ['covid','offline','diagnostic','remote']



def book(type, area_id,time_slot=None,date=None):

    booking = obj.get_appointment(area_id=area_id,type=type)


    if type == 'offline':

        booking['Message'] += date + "\n"
        booking['Booking_number'] = random.randint(0,10)
        booking['time_slot'] = time_slot

        return  booking
    elif type == 'diagnostic':

        booking['Message'] += date + "\n"
        booking['Nearest_Clinic_Message'] += date + "\n"
        booking['time_slot'] = time_slot

        return  booking
    else:

        return  booking



@appoint_ns.route('/add')
@appoint_ns.response(400,'Bad Request')
@appoint_ns.response(500,"Database Error")
class bookAppointment(Resource):
    @appoint_ns.expect(appoint)
    @appoint_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        """
        Returns a message if the appointment is successfully bookeed
        """
        try:

            payload = appoint_ns.payload
            user_id = ticket_coll.find_one({"_id":int(payload['ticket_id'])},
                                                              {"user_id":1,'_id':1})

            area_id = str(user_col.find_one({"_id":int(user_id['user_id'])},{"area_id":1})['area_id'])


            if 'date' in payload.keys():

                if 'time_slot' in payload.keys():

                    final = book(payload['type'],time_slot=payload['time_slot'],date=payload['date'],area_id=area_id)

                else:
                    final = book(payload['type'],  date=payload['date'],area_id=area_id)
            else:
                 final = book(payload['type'],area_id=area_id)

            doc= {"appointment":final,"has_appointment":True,"appointment_type":payload['type']}

            doc['currentDate']=dt.now()

            ticket_coll.update_one({"_id":payload['ticket_id']},
                                {"$set":doc})

            if payload['type'] != 'remote':

                ticket_coll.update_one({"_id":int(payload['ticket_id'])
                                   },{'$set':{'ticket_status':'closed',
                                              'currentDate':dt.now()}})



            else:
                ticket_coll.update_one({"_id": int(payload['ticket_id'])
                                        }, {'$set': {'currentDate': dt.now()}})


            return final, 200


        except:

            return {"Message":"Database Error","Error":sys.exc_info()[1]},500



@appoint_ns.route('/get')
@appoint_ns.response(400,'Bad Request')
@appoint_ns.response(500,"Database Error")
class getAppointment(Resource):
    @appoint_ns.expect(get_appoint)
    @appoint_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):

        try:
            payload = appoint_ns.payload

            doc = None


            doc = ticket_coll.find_one({"_id":payload['ticket_id'],"has_appointment":{"$exists":True}})

            if doc == None:

                return  {"Message":"No appointment Scheduled"},200
            else:
                return  {"appointment":doc['appointment'],'appointment_type':doc['appointment_type']},200

        except:

            return {"Message": "Database Error", "Error": sys.exc_info()[1]}, 500



@appoint_ns.route('/change')
@appoint_ns.response(400,'Bad Request')
@appoint_ns.response(500,"Database Error")
class changeAppointment(Resource):

    @appoint_ns.doc(security='ApiKeyAuth')
    @token_required
    @appoint_ns.expect(change_appoint)
    def post(self):
        try:

            payload = appoint_ns.payload

            user_id = ticket_coll.find_one({"_id": int(payload['ticket_id'])},
                                           {"user_id": 1, '_id': 1})

            area_id = str(user_col.find_one({"_id": int(user_id['user_id'])}, {"area_id": 1})['area_id'])


            if 'date' in payload.keys():

                if 'time_slot' in payload.keys():

                    final = book(payload['type'],time_slot=payload['time_slot'],date=payload['date'],area_id=area_id)

                else:
                    final = book(payload['type'],  date=payload['date'],area_id=area_id)
            else:
                 final = book(payload['type'],area_id=area_id)



            doc= {"appointment":final,"has_appointment":True,"appointment_type":payload['type']}



            doc['currentDate']=dt.now()

            ticket_coll.update_one({"_id": payload['ticket_id']},
                                   {"$set": doc})



            if payload['type'] != 'remote':

                ticket_coll.update_one({"_id":int(payload['ticket_id'])
                                   },{'$set':{'ticket_status':'closed',
                                              'currentDate':dt.now()}})
            return final, 200


        except:

            return {"Message":"Database Error", "Error": sys.exc_info()[1]}, 500




@appoint_ns.route('/list')
@appoint_ns.response(400,'Bad Request')
@appoint_ns.response(500,"Database Error")
class getList(Resource):

    @appoint_ns.doc(security='ApiKeyAuth')
    @token_required
    @appoint_ns.expect(list_appoint)
    def post(self):
        """
        Returns the object of nearest  appointment details
        """
        try:


            payload = appoint_ns.payload

            if payload['type'] in appoint_types:
                user_id = ticket_coll.find_one({"_id": int(payload['ticket_id'])},
                                           {"user_id": 1, '_id': 1})

                area_id = str(user_col.find_one({"_id": int(user_id['user_id'])}, {"area_id": 1})['area_id'])

                final = obj.get_appointment(area_id=area_id,type=payload['type'])

                return final,200
            else:

                return {"message":"invalid appointment type"},200

        except:

            return {"Message": "Database Error", "Error": sys.exc_info()[1]}, 500

