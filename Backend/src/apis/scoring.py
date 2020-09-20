from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
import random
from  datetime import datetime as dt
import sys
ticket_coll = db['ticket']

"""
----------------------------------------------------------------  NAMESPACE   ------------------------------------------
"""

scoring_ns = Namespace("Scoring",description="Operations related to get COVID SCORING")


scoring_params = scoring_ns.model("Get-Score",{"ticket_id":fields.Integer(required=True)})
testscoring_params = scoring_ns.model("Get-testScore",{"ticket_id":fields.Integer(required=True)
                                                       ,"covid_class":fields.String(required=True)})


covid_classes = ["High","Medium","Low"]

@scoring_ns.route("/score")
@scoring_ns.response(400,'Bad Request')
@scoring_ns.response(500,"Database Error")
class getScore(Resource):
    @scoring_ns.expect(scoring_params)
    @scoring_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        payload = scoring_ns.payload

        count = ticket_coll.count({"_id":int(payload['ticket_id'])})

        try:

            if count > 0 :
                #ticket exists


                #logic of scoring model should go here
                #should fetch the area statistics from the area collection to use it in the scoring model
                val = random.randint(0,2)
                final = {"covid_class": "Low",
                         "covid_score": random.randint(0, 100),
                         'currentDate': dt.now(),
                         'ticket_status': "consulting"
                         }

                ticket_coll.update_one({"_id": payload['ticket_id']}, {"$set": final})

                return final,200

            else:
                return {"message":"Ticket not found"},200

        except:

                return {"message":"Database Error"} , 500



#test api

@scoring_ns.route("/testscore")
@scoring_ns.response(400,'Bad Request')
@scoring_ns.response(500,"Database Error")
class gettestScore(Resource):
    @scoring_ns.expect(testscoring_params)
    @scoring_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        payload = scoring_ns.payload

        count = ticket_coll.count({"_id":payload['ticket_id']})

        try:

            if count > 0 :
                #ticket exists


                #logic of scoring model should go here
                #should fetch the area statistics from the area collection to use it in the scoring model

                if payload['covid_class'] in covid_classes:
                    final = { "covid_class" : "Low",
                          "covid_score": random.randint(0,100),
                              'currentDate' : dt.now(),
                              'ticket_status':"consulting"
                    }

                 #updating the ticket
                    ticket_coll.update_one({"_id":payload['ticket_id']},{"$set":final})

                    return final,200
                else:

                    return {"message":"Invalid Covid Class"}
            else:
                return {"message":"Ticket not found"},200

        except:

                return {"message":"Database Error","error":sys.exc_info()[1]} , 500


