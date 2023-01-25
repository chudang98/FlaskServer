import logging

from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from auth.jwt_utils import token_required, create_token

load_dotenv('./.env')
server_api = Flask(__name__)

@server_api.route('/api/home', methods=['GET'])
def home_api():
  return jsonify({
    'message': 'Hello baby !!!!!'
  })

@server_api.route('/api/auth', methods=['GET'])
@token_required
def test_token(data):
  return jsonify({
    'data': data,
    'message': 'Hello baby !!!!!'
  })

@server_api.route('/api/signup', methods=['POST'])
def sign_up():
  payload = request.json
  logging.warning(payload)
  return jsonify({
    'data': create_token(payload),
    'message': 'Create token success.'
  })
