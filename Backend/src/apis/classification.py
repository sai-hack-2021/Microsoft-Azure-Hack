from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
from datetime import datetime as dt
import requests
import sys
ticket_coll = db['ticket']


classifier_ns = Namespace("Classification",description="Operations related to Fever Classification")


classifier_params = classifier_ns.model("Get-class",{"ticket_id":fields.String(required=True)})

testclassifier_params = classifier_ns.model("Get-testclass",{"ticket_id":fields.Integer(required=True)
                                                       ,"fever_class":fields.String(required=True)})



fever_classes = ["Bacterial","Malarial","Viral"]

url='http://feverclassification-ars.centralindia.azurecontainer.io/api/Classifier/classify'


def parse_symptoms(data):
    body = {
        "body-Temp": 0,
        "type-of-fever": 0,
        "type-of-bodypain": 0,
        "loose-motion": 0,
        "vomiting": 0,
        "cough": 0,
        "cold": 0,
        "urinary-irritation": 0
    }

    if 'ui' in data:
        body['urinary-irritation'] = data['ui']
    if 'vomit' in data:
        body['vomiting'] = data['vomit']
    if 'diarrhea' in data:
        body['loose-motion'] = data['diarrhea']
    if 'fever_type' in data:
        body['type-of-fever'] = data['fever_type']
    if 'body_pain_type' in data:
        if data['body_pain_type'] != 4:
            body['type-of-bodypain'] = data['body_pain_type']
    if 'fever_temp' in data:
        if data['fever_temp'] == 1:
            body['body-Temp'] = 99.5
        elif data['fever_temp'] == 2:
            body['body-Temp'] = 101.5
        elif data['fever_temp'] == 3:
            body['body-Temp'] = 102.5
    if 'cough' in data:
        body['cough'] = data['cough']
    if 'cold' in data:
        body['cold'] = data['cold']

    return body


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

                doc = ticket_coll.find_one({"_id":int(payload['ticket_id'])})

                if "symptoms" in doc:

                    body =  parse_symptoms(doc['symptoms']['symptoms'])

                    val = requests.post(url=url, json=body ,headers={"auth-key": "azurehackml"})
                    val = val.json()['fever'].lower().capitalize()



                final = {"predicted_fever_class": "Malarial", 'currentDate': dt.now()
                         }

                # updating the ticket
                ticket_coll.update_one({"_id": int(payload['ticket_id'])}, {"$set": final})

                return final, 200


            else:
                return {"message":"Ticket not found"},200

        except:

                return {"message":"Database Error","error":sys.exc_info()[1]} , 500


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

                return {"message":"Database Error","error":sys.exc_info()[1]} , 500


