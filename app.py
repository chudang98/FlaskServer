import logging
from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
from routes.auth_routes import auth_routes
from routes.project_routes import project_routes

load_dotenv('./.env')

# MONGODB_URL = environ.get('MONGODB_URL')
MONGODB_URL = "mongodb://admin:password@mongodb:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
# MONGODB_URL = "mongodb://admin:password@localhost:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
connect(host=MONGODB_URL)
logging.warning(MONGODB_URL)

server_api = Flask(__name__)

server_api.register_blueprint(auth_routes)
server_api.register_blueprint(project_routes)
# CORS(server_api)

if __name__ == "__main__":
    server_api.run(host='0.0.0.0', port=443, debug=True,
                        ssl_context=('/app/cert/cert.pem', '/app/cert/key.pem')
                   )
