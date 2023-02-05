from flask import Blueprint, jsonify, request, make_response
from auth.authen import token_required, create_token, bcrypt_password, check_password
import logging
from models.projects import Project

project_routes = Blueprint(
  'project_routes',
  __name__,
  url_prefix='/api/projects'
)

@project_routes.route('/add', methods=['POST'])
@token_required
def add_projects(*arg, **kwargs):
  # Check projects is exist
  print(kwargs)
  user = kwargs['user_info']
  print(user)
  # Add project to DB
  return jsonify({
    'data': 'Access !',
    'message': 'Hello baby !!!!!'
  })
