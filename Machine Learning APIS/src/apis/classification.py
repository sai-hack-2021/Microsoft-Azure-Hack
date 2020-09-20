from flask_restplus import  Resource, fields,Namespace
from src import token_required
import sys
from src.apis.MLmodule import Machine_learning


obj = Machine_learning() #loading model


classifier_ns = Namespace("Classification",description="Operations related to Fever Classification")


classifier_params = classifier_ns.model("Get-class",{

    "body-Temp":fields.Float(required=True),
    "type-of-fever": fields.Integer(required=True),
    "type-of-bodypain": fields.Integer(required=True),
    "loose-motion": fields.Integer(required=True),
    "vomiting":fields.Integer(required=True),
    "cough": fields.Integer(required=True),
    "cold": fields.Integer(required=True),
    "urinary-irritation": fields.Integer(required=True)
                                        })


def validated_params(payload):

    if (payload['type-of-fever']  > 2) :
        return  {'type-of-fever': "Value cannot be greater than 2"}
    if (payload['type-of-bodypain'] > 3) :
        return {'type-of-bodypain':"Value cannot be greater than 3"}
    if (payload['cough'] > 3) :
        return {"cough": "Value cannot be greater than 3"}
    if (payload['cold'] > 2):
        return {"cold":"Value cannot be greater than 2"}
    if (payload['vomiting']>1):
        return {"vomiting":"Value can either be 1 or 0"}
    if (payload['loose-motion']>1):
        return {"loose-motion":"Value can either be 1 or 0"}
    if (payload['urinary-irritation'] > 1):
        return {"urinary-irritation": "Value can either be 1 or 0"}
    if isinstance(payload['body-Temp'],float):
        pass
    else:
        return {"body-Temp":"Value must be a float value"}

    return True





@classifier_ns.route("/classify")
@classifier_ns.response(400,'Bad Request')
@classifier_ns.response(500,"Database Error")
class getClass(Resource):
    @classifier_ns.expect(classifier_params)
    @classifier_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):
        payload = classifier_ns.payload

        try:

           value = validated_params(payload)
           if isinstance(value,bool):
               obj.setValues(Temp = payload['body-Temp'],TOF=payload['type-of-fever'],bpain=payload['type-of-bodypain'],
                             VOM=payload['vomiting'],LM=payload['loose-motion'],COU=payload['cough'],COLD=payload['cold'],Ui=payload['urinary-irritation'])

               return {"fever":obj.predictValues()},200
           else:

               return value,200


        except:

                return {"message":"Database Error","Error":sys.exc_info()[1]} , 500


#test api


