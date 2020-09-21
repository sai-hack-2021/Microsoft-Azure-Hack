from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
from datetime import datetime as dt, timedelta
import sys


collection_name = 'ticket'
collection = db[collection_name]




ticket_status = ['open','consulting','in-progress','monitoring','closed']

ticket_ns = Namespace("ticket",description="Operations related to test-ticket for UI development")

create_ticket = ticket_ns.model("create_ticket",{
    'user_id':fields.Integer(requied=True)
})

update_ticket = ticket_ns.model("update_ticket_status",{
    "ticket_id": fields.Integer(required=True),
    "ticket_status":fields.String(required=True),
    "monitoring_days": fields.Integer()
})

feedback = ticket_ns.model("feedback",{
    "ticket_id":fields.Integer(required=True),
    "feedback":fields.String(required=True),
"monitoring_days": fields.Integer(),
    "ticket_close":fields.Boolean(required=True)

})



@ticket_ns.route('/<id>')
@ticket_ns.response(400,'Bad Request')
@ticket_ns.response(500,"Database Error")
class getTicket(Resource):
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def get(self,id):
        """
        Returns the user details when routed through the given user_id
        """

        try:

            value = collection.find_one({'_id':int(id)})

            if value :

                value['ticket_id'] = value['_id']
                del value['_id']

                return value,200
            else:
                return {"message":"Ticket not Found"},401
        except:

            return  {"message":"Database Error"}, 500


@ticket_ns.route('/create')
@ticket_ns.response(400, 'Bad Request')
@ticket_ns.response(200, "Successful insertion")
@ticket_ns.response(500, "Database Error")
class createTicket(Resource):
    @ticket_ns.expect(create_ticket)
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        """
        Returns the created ticket id After successful insertion
        """

        try:

            payload = ticket_ns.payload

            count = collection.count_documents({"user_id":int(payload['user_id']),"ticket_status":{"$ne":"closed"}})

            if count == 0 :

                payload['ticket_status'] = 'open' #making open status
                payload['created_at'] = dt.now()
                payload['currentDate'] = payload['created_at']
                payload['_id'] = generatenextseqval(collection_name, db)
                payload["monitoring_days"]= 0

                collection.insert_one(payload)

                return {"ticket_id":payload['_id']},200
            else:

                return {"message":"Already has a open ticket"} , 200
        except:

            return {"message": "Database Error"}, 500


@ticket_ns.route('/status/<id>')
@ticket_ns.response(400,'Bad Request')
@ticket_ns.response(401,"Ticket not found")
@ticket_ns.response(500,"Database Error")

class getTicketStatus(Resource):
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def get(self,id):
        """
        Returns the status of the ticket id
        """

        try:
            value = collection.find_one({'_id': int(id)},{"ticket_status":1,"_id":0})

            if value :
                return value,200
            else:
                return {"message":"Ticket not Found"},401
        except:

            return  {"message":"Database Error"}, 500


@ticket_ns.route('/status/update')
@ticket_ns.response(400, 'Bad Request')
@ticket_ns.response(200, "Update has been successful")
@ticket_ns.response(500, "Database Error")


class updateTicketStatus(Resource):

    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    @ticket_ns.expect(update_ticket)
    def post(self):

        """
        Returns the message success on correct successful updation
        """

        payload = ticket_ns.payload

        try:

            if payload['ticket_status'] in ticket_status:

                if payload['ticket_status'] != 'monitoring':

                    collection.update_one({"_id":int(payload['ticket_id']),
                                          },{'$set':{'ticket_status':payload['ticket_status'],
                                              'currentDate':dt.now() }})
                else:

                    if 'monitoring_days' in payload:

                        collection.update_one({"_id": int(payload['ticket_id']),
                                               }, {'$set': {'ticket_status': payload['ticket_status'],
                                                            'currentDate': dt.now() + timedelta(days=int(payload['monitoring_days'])
                                                                                )}})
                        return {"message": "Successfully Updated"}, 200

                    else:

                        return {"message":"The status is monitoring and the monitoring_days parameter is missing"},200


                return {"message": "Successfully Updated"}, 200
            else:

                return {"message":"Status not defined"},400

        except:

            return {"Database Error":sys.exc_info()[1]},500



@ticket_ns.route('/latest')
@ticket_ns.response(400, 'Bad Request')
@ticket_ns.response(200, "Successful")
@ticket_ns.response(401,"No record for this user")
@ticket_ns.response(500, "Database Error")
class getLatestTicket(Resource):
    @ticket_ns.expect(create_ticket)
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        """
        Returns the latest ticket which is not closed
        """

        payload = ticket_ns.payload



        try:
            final = collection.find({'user_id':payload['user_id']},limit=2).sort([('currentDate',-1)])[0]

            if final:

                final['ticket_id'] = final['_id']
                del final['_id']

                return {"latest_ticket": final}, 200
            else:

                return {"latest_ticket": False}, 401
        except:

            return {"message":"Database Error", "Error":sys.exc_info()[1]},500



@ticket_ns.route('/history')
@ticket_ns.response(400,'Bad Request')
@ticket_ns.response(200, 'Successful')
@ticket_ns.response(500, "Database Error")
class getTicketHistory(Resource):
    @ticket_ns.expect(create_ticket)
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required

    def post(self):
        """
        Returns the list of tickets raised in the past
        """
        payload = ticket_ns.payload


        try:

            final = []

            for i in collection.find({"user_id":int(payload['user_id'])}).sort([('currentDate',-1)]):

                i['ticket_id'] = i.pop('_id')
                final.append(i)

            if final:

                return {"history": final}, 200
            else:

                return {"history":[]},200
        except:

            return {"message": "Database Error", "Error": sys.exc_info()[1]}, 500



@ticket_ns.route('/symptoms/update')
@ticket_ns.response(400,'Bad Request')
@ticket_ns.response(200, 'Successful')
@ticket_ns.response(500, "Database Error")
class updateSymptoms(Resource):
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):

        """
        Returns as message success after successful updation
        """
        payload = ticket_ns.payload

        #parsing

        try:
            if "covid_status" in payload['symptoms']['symptoms'] :

                if payload['symptoms']['symptoms']["covid_status"] == 'Low Risk - No Fever':
                    collection.update_one({"_id": int(payload['ticket_id'])},
                                      {"$set": {"symptoms": payload['symptoms'], "ticket_status": "closed"}})
                else:

                    collection.update_one({"_id": int(payload['ticket_id'])},
                                          {"$set": {"symptoms": payload['symptoms']}})
            else:

                collection.update_one({"_id":int(payload['ticket_id'])},{"$set":{"symptoms":payload['symptoms'],"ticket_status":"in-progress"}})


            return {'message':'success'},200
        except:
            return {"message":"Database Error"},500


@ticket_ns.route('/symptoms/<id>')
@ticket_ns.response(200, 'Successful')
@ticket_ns.response(500, "Database Error")
class getSymptioms(Resource):
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    def get(self,id):
        """
        Returns a dictionary of symptoms:
        """

        try:

            symptoms = collection.find_one({"_id":int(id)},{"symptoms":1,"_id":1})


            if isinstance(symptoms,dict):


                return symptoms,200
            else:
                return {"message":"Symptoms not yet updated"},200

        except:
            return {"message": "Database Error"}, 500


@ticket_ns.route("/feedback")
@ticket_ns.response(400,'Bad Request')
@ticket_ns.response(200, 'Successful')
@ticket_ns.response(500, "Database Error")
class putFeedback(Resource):
    @ticket_ns.doc(security='ApiKeyAuth')
    @token_required
    @ticket_ns.expect(feedback)
    def post(self):
        """
        Returns a succesfull message when updated
        """

        payload = ticket_ns.payload

        val = {
            "feedback":payload['feedback'],
            "currentDate":dt.now()
        }

        if payload['ticket_close']:

            val['ticket_status'] = "closed"
        else:

            if payload['monitoring_days'] != 0:

                val['ticket_status'] = "monitoring"
                val['monitoring_days'] = payload['monitoring_days']

        try:
            collection.update_one({"_id":int(payload["ticket_id"])},{"$set":val})

            return {"messsage":"successful feedback"},200

        except:

            return {"message":"Database Error","error":sys.exc_info()[1]}

