from flask import Flask, Blueprint
from flask_restplus import Api
from flask_cors import CORS
from src.apis.classification import  classifier_ns
authorisations = {
     'ApiKeyAuth':{
        'type':'apiKey',
         'in':'header',
         'name':'auth-key'
     }
}


api_bp = Blueprint('api', __name__)
#cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})
api = Api(api_bp, title='Fever Classification Machine learning model',
          version='1.0',
          description='Functional APIs to get all the necessary functions ',
          doc='/api/documentation',
          authorizations=authorisations,security='ApiKeyAuth')

api.add_namespace(classifier_ns,path="/api/Classifier")
application = Flask(__name__)
application.register_blueprint(api_bp)
cors = CORS(application,resources={r"/api/*": {"origins": "*"}})

application.config['CORS_HEADERS'] = 'Content-Type'






if __name__ == "__main__":
    """
    running the application

    """


    application.run(host="0.0.0.0", port= 5000,debug = True)
