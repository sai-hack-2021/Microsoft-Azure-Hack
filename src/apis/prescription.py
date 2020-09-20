from flask_restplus import  Resource, fields,Namespace
from src import token_required
from src import db ,generatenextseqval
import sys
import datetime as dt

ticket_coll = db['ticket']


pres_ns = Namespace("Prescription",description="Operations related to Appointments")



@pres_ns.route('/add')
@pres_ns.response(400,'Bad Request')
@pres_ns.response(200, 'Successful')
@pres_ns.response(500, "Database Error")
class updatePrescription(Resource):
    @pres_ns.doc(security='ApiKeyAuth')
    @token_required
    def post(self):

        """
        Returns as message success after successful updation
        """
        payload = pres_ns.payload

        #parsing

        try:

            ticket_coll.update_one({"_id":int(payload['ticket_id'])},{"$set":{"prescription":payload['prescription'],
                                                                              "has_prescription":True}})


            return {'message':'success'},200
        except:
            return {"message":"Database Error","error":sys.exc_info()[1],"payload":payload},500



@pres_ns.route('/<id>')
@pres_ns.response(200, 'Successful')
@pres_ns.response(500, "Database Error")
class getPrescription(Resource):
    @pres_ns.doc(security='ApiKeyAuth')
    @token_required
    def get(self,id):
        """
        Returns a dictionary of symptoms:
        """
        try:

            pres = ticket_coll.find_one({"_id":int(id)},{"prescription":1})
            return pres,200

        except:
            return {"message": "Database Error"}, 500



