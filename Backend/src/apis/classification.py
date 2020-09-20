from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
from datetime import datetime as dt
import random
url = ''

ticket_coll = db['ticket']


classifier_ns = Namespace("Classification",description="Operations related to Fever Classification")


classifier_params = classifier_ns.model("Get-class",{"ticket_id":fields.String(required=True)})

testclassifier_params = classifier_ns.model("Get-testclass",{"ticket_id":fields.Integer(required=True)
                                                       ,"fever_class":fields.String(required=True)})



fever_classes = ["Bacterial","Malarial","Viral"]


@classifier_ns.route("/classify")
@classifier_ns.response(400,'Bad Request')
@classifier_ns.response(500,"Database Error")
class getClass(Resource):
    @classifier_ns.expect(classifier_params)
    @classifier_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        payload = classifier_ns.payload

        count = ticket_coll.count({"_id":int(payload['ticket_id'])})

        try:

            if count > 0 :
                #ticket exists


                #logic of classifier model should go here
                #should fetch the area statistics from the area collection to use it in the classifier model
                val = random.randint(0,2)
                final = {"predicted_fever_class": "Bacterial", 'currentDate': dt.now()
                         }

                # updating the ticket
                ticket_coll.update_one({"_id": payload['ticket_id']}, {"$set": final})

                return final, 200


            else:
                return {"message":"Ticket not found"},200

        except:

                return {"message":"Database Error"} , 500


#test api

@classifier_ns.route("/testclassify")
@classifier_ns.response(400,'Bad Request')
@classifier_ns.response(402,"This Fever class is not allowed")
@classifier_ns.response(500,"Database Error")
class getTestClass(Resource):
    @classifier_ns.expect(testclassifier_params)
    @classifier_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        payload = classifier_ns.payload

        count = ticket_coll.count({"_id":int(payload['ticket_id'])})

        try:

            if count > 0 :
                #ticket exists

                if payload['fever_class'] in fever_classes:

                    final = { "predicted_fever_class" : payload['fever_class'],'currentDate' : dt.now()
                    }

                    #updating the ticket
                    ticket_coll.update_one({"_id":payload['ticket_id']},{"$set":final})

                    return final,200
                else:
                    return {"message":"Invalid Fever Class"},200

            else:
                return {"message":"Ticket not found"},200

        except:

                return {"message":"Database Error"} , 500


