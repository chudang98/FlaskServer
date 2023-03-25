import logging
from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
from routes.auth_routes import auth_routes
from routes.project_routes import project_routes
# from flask_cors import CORS

load_dotenv('./.env')

# MONGODB_URL = environ.get('MONGODB_URL')
MONGODB_URL = "mongodb://admin:password@mongodb:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
# MONGODB_URL = "mongodb://admin:password@localhost:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
connect(host=MONGODB_URL)
logging.warning(MONGODB_URL)

server_api = Flask(__name__)

server_api.register_blueprint(auth_routes)
server_api.register_blueprint(project_routes)

# CORS(server_api, resources=r"/api/*")
# CORS(server_api)
# logging.getLogger('flask_cors').level = logging.DEBUG

# CORS(server_api, resources={r"/api/*": {"origins": "*"}})

# CORS(server_api, resources={r"/api/*": {
#     "origins": "*",
#     # "supports_credentials": True,
#     "allow_headers": "*",
#     "methods":  ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
#     "send_wildcard": "*"
#     }
#   })

if __name__ == "__main__":
    server_api.run(host='0.0.0.0', port=5000,
                   # debug=True,
                        ssl_context=('/app/cert/cert.pem', '/app/cert/key.pem')
                   )
    # CORS(server_api, resources=r"/api/*")
    # CORS(server_api, resources={r"/api/*": {
    #   "origins": "*",
    #   # "supports_credentials": True,
    #   "allow_headers": "*",
    #   "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    #
    #   "send_wildcard": "*"
    # }
    # })
