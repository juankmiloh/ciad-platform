from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from source_controller import SourceController

context = ('server.crt', 'server.key')

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})

CORS(app, resources={r"/pqr/*": {"origins": "*"}})
CORS(app, resources={r"/empresa/*": {"origins": "*"}})
CORS(app, resources={r"/causas/*": {"origins": "*"}})
CORS(app, resources={r"/pqr_causas/*": {"origins": "*"}})
CORS(app, resources={r"/anios/*": {"origins": "*"}})

CORS(app, resources={r"/i_anios/*": {"origins": "*"}})
CORS(app, resources={r"/i_causas/*": {"origins": "*"}})
CORS(app, resources={r"/i_empresas/*": {"origins": "*"}})
CORS(app, resources={r"/i_interrupcion/*": {"origins": "*"}})

CORS(app, resources={r"/tarifarito/api/*": {"origins": "*"}})

CORS(app, supports_credentials=True)

SourceController (api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, ssl_context=context, threaded=True, debug=True)
