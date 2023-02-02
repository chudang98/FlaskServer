from functools import wraps
import jwt
from flask import request, jsonify
from os import environ
import logging
from datetime import datetime, timedelta
import bcrypt
from models.user import User

SECRET_JWT = environ.get('SECRET_JWT')
SALT = environ.get('SECRET_SALT_PWD')
TIME_EXPIRE = 150
# TODO: Middleware for route need token
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    logging.warning("Check JWT token...")
    # jwt is passed in the request header
    if 'x-access-token' in request.headers:
      logging.warning('Have X-Access-Token !')
      token = request.headers['x-access-token']
    # return 401 if token is not passed
    if not token:
      return jsonify({'message': 'Token is missing !!'}), 401
    try:
      logging.warning('Decode JWT token...')
      # decoding the payload to fetch the stored details
      data = jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
      user = User.objects.get(
        username=data['username'],
        email=data['email']
      )
      if not user:
        raise Exception('Username or email not found !')

    except Exception as e:
      logging.warning(e)
      return jsonify({
        'message': 'Check JWT token error !!'
      }), 401
    # returns the current logged in users contex to the routes
    return f(*args, **kwargs)

  return decorated

def create_token(payload_args):
  return jwt.encode(
    payload={
      **payload_args,
      'exp': datetime.utcnow() + timedelta(days=TIME_EXPIRE),
      'iat': datetime.utcnow()
    },
    key=SECRET_JWT,
    algorithm='HS256'
  )

def bcrypt_password(password):
  return bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
  ).decode('utf-8')

def check_password(pwd_input, pwd_bcrypt):
  return bcrypt.checkpw(
    pwd_input.encode('utf-8'),
    pwd_bcrypt.encode('utf-8')
  )