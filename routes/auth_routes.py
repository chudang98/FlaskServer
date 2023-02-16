from flask import Blueprint, jsonify, request, make_response
from auth.authen import token_required, create_token, bcrypt_password, check_password
import logging
from models.user import User
import json

auth_routes = Blueprint(
  'auth_routes',
  __name__,
  url_prefix='/api'
)

@auth_routes.route('/home', methods=['GET'])
def home_api(*args, **kwargs):
  return jsonify({
    'message': 'Hello baby !!!!!'
  })

@auth_routes.route('/auth', methods=['GET'])
@token_required
def test_token(*arg, **kwargs):
  return jsonify({
    'data': 'Access !',
    'message': 'Hello baby !!!!!'
  })

@auth_routes.route('/signup', methods=['POST'])
def sign_up(*args, **kwargs):
  try:
    payload = request.json
    new_user = User(
      username=payload.get('username'),
      email=payload.get('email'),
      password=bcrypt_password(payload.get('password'))
    )
    new_user.save()
    # logging.warning(payload)
    return jsonify({
      'token': create_token({
        'username': payload.get('username'),
        'email': payload.get('email')
      }),
      'message': 'Create token success.'
    })
  except Exception as e:
    logging.error("API Signup have error !")
    logging.error(e)
    return make_response(
      jsonify({
        'error': 'Sign up failed !'
      }),
      400
    )

@auth_routes.route('/login', methods=['POST'])
def login(*args, **kwargs):
  try:
    payload = request.json
    username = payload.get('username')
    pwd = payload.get('password')
    user = User.objects.get(username=username)
    if not check_password(pwd, user['password']):
      raise Exception('Password wrong !')

    return jsonify({
      'token': create_token({
        'username': username,
        'email': user['email']
      }),
      'message': 'Create token success.'
    })
  except Exception as e:
    logging.error("API Login have error !")
    logging.error(e)
    return make_response(
      jsonify({
        'error': 'Login failed !'
      }),
      400
    )

@auth_routes.route('/test', methods=['GET'])
def test_api(*args, **kwargs):
  return jsonify({
    'message': 'This is test !!!!!'
  })

@auth_routes.route('/profile', methods=['GET'])
@token_required
def get_profile(*args, **kwargs):
  user = kwargs.get('user_info')
  user_profile = json.loads(user.to_json())
  del user_profile['_id']
  del user_profile['password']
  return jsonify({
    'data': user_profile
  })