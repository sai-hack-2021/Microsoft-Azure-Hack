from flask import Flask, Blueprint
from src.apis.users import user_ns
from src.apis.ticket import ticket_ns
from src.apis.scoring import scoring_ns
from src.apis.classification import classifier_ns
from src.apis.prescription import pres_ns
from src.apis.appointment import appoint_ns
import atexit
from flask_restplus import Api
from flask_cors import CORS

authorisations = {
     'ApiKeyAuth':{
        'type':'apiKey',
         'in':'header',
         'name':'auth-key'
     }
}


api_bp = Blueprint('api', __name__)
#cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})
api = Api(api_bp, title='Online Health-Aid',
          version='1.0',
          description='Functional APIs to get all the necessary functions ',
          doc='/api/documentation',
          authorizations=authorisations,security='ApiKeyAuth')

api.add_namespace(user_ns, path="/api/Users")
api.add_namespace(ticket_ns,path="/api/Tickets")
api.add_namespace(scoring_ns,path="/api/Scoring")
api.add_namespace(classifier_ns,path="/api/Classifier")
api.add_namespace(pres_ns,path="/api/Prescription")
api.add_namespace(appoint_ns,path='/api/Appointment')
application = Flask(__name__)
application.register_blueprint(api_bp)
cors = CORS(application,resources={r"/api/*": {"origins": "*"}})

application.config['CORS_HEADERS'] = 'Content-Type'



def close_db():
    """
    closing the db pools in mongdo
    """

    print("Closing Mongo connection \n")

    from src import connection
    connection.close()


atexit.register(close_db)


if __name__ == "__main__":
    """
    running the application

    """


    application.run(host="0.0.0.0", port= 5000,debug = True)
