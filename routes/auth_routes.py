from flask import Blueprint, jsonify, request
from auth.authen import token_required, create_token, hash_password
import logging
from models.user import User

auth_route = Blueprint(
  'auth_routes',
  __name__,
  url_prefix='/api'
)

@auth_route.route('/home', methods=['GET'])
def home_api():
  return jsonify({
    'message': 'Hello baby !!!!!'
  })

@auth_route.route('/auth', methods=['GET'])
@token_required
def test_token(data):
  return jsonify({
    'data': data,
    'message': 'Hello baby !!!!!'
  })

@auth_route.route('/signup', methods=['POST'])
def sign_up():
  try:
    payload = request.json
    new_user = User(
      username=payload.get('username'),
      email=payload.get('email'),
      password=payload.get('password')
    )
    new_user.save()
    # logging.warning(payload)
    return jsonify({
      'data': create_token(payload),
      'message': 'Create token success.'
    })
  except Exception as e:
    logging.error("API Signup have error !")
    logging.error(e)

@auth_route.route('/test', methods=['GET'])
def test_api():
  return jsonify({
    'message': 'This is test !!!!!'
  })