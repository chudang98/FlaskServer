from flask import Blueprint, jsonify, request
from auth.authen import token_required
import logging
from models.projects import Project
from models.user import User
import json
import time
from datetime import datetime

project_routes = Blueprint(
  'project_routes',
  __name__,
  url_prefix='/api/projects'
)

@project_routes.route('', methods=['GET'])
@token_required
def list_projects(*arg, **kwargs):
  user = kwargs.get('user_info')
  print(user['projects'])
  data = [
    {
      'id': str(project['id']),
      'link': project['link'],
      'project_name': project['project_name'],
      'frequency':  project['frequency'],
      'created_time': datetime.timestamp(project['created_time']),
      'updated_time':datetime.timestamp(project['updated_time'])
    }
    for project in user['projects']
  ] if len(user['projects']) > 0 else []
  print(data)
  return jsonify({
    'data': data,
    'length': len(data),
    'message': 'Get list projects success !'
  })

@project_routes.route('', methods=['POST'])
@token_required
def add_projects(*arg, **kwargs):
  payload = request.json
  link_projects_request = payload.get('projects')
  user = kwargs['user_info']
  list_project = [project['link'] for project in user['projects']]
  links_project_req = [project['link'] for project in link_projects_request]
  for link_project in links_project_req:
    if link_project in list_project:
      logging.warning('Project is existed !!!')
      return jsonify({
        'message': f'Project {link_project} is existed for this user !!'
      }), 401

  for project in link_projects_request:
    project = Project(
      link=project['link'],
      project_name=project['link'].split("https://twitter.com/", 1)[1],
      frequency=project['frequency']
    )
    try:
      project.save()
    except Exception as e:
      logging.error("Add project have error !")
      logging.error(e)

    User.objects(id=user['id']).update_one(push__projects=project)

  # Add project to DB
  return jsonify({
    'message': 'Add projects success !'
  })

@project_routes.route('', methods=['DELETE'])
@token_required
def delete_project(*arg, **kwargs):
  payload = request.json
  id_project = payload.get('project')
  user = kwargs['user_info']
  project = Project.objects.get(id=id_project)
  User.objects(id=user['id']).update_one(pull__projects=project)
  Project.objects(id=id_project).delete()
  # Add project to DB
  return jsonify({
    'message': 'Delete projects success !'
  })