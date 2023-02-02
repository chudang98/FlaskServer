import logging

from flask import Flask
from dotenv import load_dotenv
from os import environ
from mongoengine import connect
from routes.auth_routes import auth_route

# MONGODB_URL = environ.get('MONGODB_URL')
MONGODB_URL = "mongodb://admin:password@mongodb:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
connect(host=MONGODB_URL)
logging.warning(MONGODB_URL)

load_dotenv('./.env')
server_api = Flask(__name__)
server_api.register_blueprint(auth_route)

if __name__ == "__main__":
    server_api.run(host='0.0.0.0', port=5000, debug=True)
