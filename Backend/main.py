from flask import Flask
from flask_cors import CORS
from flask_restful import Api, reqparse
from source_controller import SourceController


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/pqr/*": {"origins": "*"}})
CORS(app, resources={r"/empresa/*": {"origins": "*"}})
CORS(app, resources={r"/causas/*": {"origins": "*"}})
CORS(app, resources={r"/pqr_causas/*": {"origins": "*"}})
CORS(app, resources={r"/anios/*": {"origins": "*"}})

SourceController (api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
