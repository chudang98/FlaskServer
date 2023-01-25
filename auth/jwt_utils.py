from functools import wraps
import jwt
from flask import request, jsonify
from os import environ
import logging
from datetime import datetime, timedelta

SECRET_JWT = environ.get('SECRET_JWT')
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
    except:
      return jsonify({
        'message': 'Check JWT token error !!'
      }), 401
    # returns the current logged in users contex to the routes
    return f(data, *args, **kwargs)

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
