from flask import Blueprint, jsonify, request, make_response
from auth.authen import token_required, create_token, bcrypt_password, check_password
import logging
from models.projects import Project
from models.user import User
import json

project_routes = Blueprint(
  'project_routes',
  __name__,
  url_prefix='/api/projects'
)

@project_routes.route('/', methods=['GET'])
@token_required
def list_projects(*arg, **kwargs):
  user = kwargs.get('user_info')
  print(user)
  data = [
    json.loads(project.to_json())
    for project in user['projects']
  ] if len(user['projects']) > 0 else []
  return jsonify({
    'data': data,
    'length': len(data),
    'message': 'Get list projects success !'
  })


@project_routes.route('/add', methods=['POST'])
@token_required
def add_projects(*arg, **kwargs):
  payload = request.json
  link_projects_request = payload.get('projects')
  user = kwargs['user_info']
  list_project = user['projects']
  for project in list_project:
    if project['link'] in link_projects_request:
      logging.warning('Project is existed !!!')
      return jsonify({
        'message': f'Project {project["link"]} is existed for this user !!'
      }), 401

  for link in link_projects_request:
    project = Project(
      link=link,
      project_name=link.split("https://twitter.com/", 1)[1]
    )
    try:
      project.save()
    except Exception as e:
      logging.error("Add project have error !")
      logging.error(e)
      project = Project.objects.get(link=link)

    User.objects(id=user['id']).update_one(push__projects=project)

  # Add project to DB
  return jsonify({
    'message': 'Add projects success !'
  })

@project_routes.route('/delete', methods=['DELETE'])
@token_required
def delete_project(*arg, **kwargs):
  payload = request.json
  id_project = payload.get('project')
  user = kwargs['user_info']
  project = Project.objects.get(id=id_project)
  User.objects(id=user['id']).update_one(pull__projects=project)
  # Add project to DB
  return jsonify({
    'message': 'Delete projects success !'
  })