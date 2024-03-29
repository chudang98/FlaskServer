from flask import Blueprint, jsonify, request, g
from auth.authen import token_required
import logging
from models.projects import Project
from models.user import User
import json
import time
from datetime import datetime
from utils.docker import create_container
# from utils.bigquery import add_read_project_id_permission
import re
from utils.scheduler import add_schedule_job

project_routes = Blueprint(
  'project_routes',
  __name__,
  url_prefix='/api/projects'
)

@project_routes.route('', methods=['GET'])
@token_required
def list_projects(*arg, **kwargs):
  user = kwargs.get('user_info')
  logging.warning("Get list project of user...")
  logging.warning(user['projects'])
  data = [
    {
      'id': str(project['id']),
      'link': project['link'],
      'project_name': project['project_name'],
      'frequency':  project['frequency'],
      'status': project['status'],
      'created_time': datetime.timestamp(project['created_time']),
      'updated_time': datetime.timestamp(project['updated_time']),
      'last_run': datetime.timestamp(project['last_run'])
    }
    for project in user['projects']
  ] if len(user['projects']) > 0 else []
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

  # TODO: Check link existed
  for link_project in links_project_req:
    if link_project in list_project:
      logging.warning('Project is existed !!!')
      return jsonify({
        'message': f'Project {link_project} is existed for this user !!'
      }), 401
    try:
      re.search('(?<=\/\/twitter.com\/)([a-zA-Z0-9]{1,})', link_project).group()
    except Exception as e:
      return jsonify({
        'message': f'Project {link_project} have wrong url !!'
      }), 401
  message_res = []
  for project in link_projects_request:
    try:
      username = project['link'].split("https://twitter.com/", 1)[1]
      project = Project(
        link=project['link'],
        project_name=username,
        frequency=project['frequency'],
        status="RUNNING"
      )
      project.save()
      saved_project = Project.objects.get(id=project.id)
      logging.warning("Start run container crawl timeline...")
      create_container(project.id, project['link'], user['email'])
      add_schedule_job(g.scheduler_crawler, {
        'project_name': username,
        'project_id': project.id,
        'frequence': project['frequency'],
        'link': project['link']
      })
      user.projects.append(saved_project)
      # api_get_id = get_profile_twitter(username)
      # id_project = api_get_id.json()['data']['id']
      # list_proj_ids.append(id_project)
      # User.objects(id=user['id']).update_one(push__projects=saved_project)
    except Exception as e:
      message_res.append(project['link'])
      logging.error("Add project have error !")
      logging.error(e)
  user.save()
  # filter_list = list(dict.fromkeys(list_proj_ids))
  # add_read_project_id_permission(filter_list, user['email'])
  list_project_user = [
    {
      'id': str(project['id']),
      'link': project['link'],
      'project_name': project['project_name'],
      'frequency':  project['frequency'],
      'status': project['status'],
      'created_time': datetime.timestamp(project['created_time']),
      'updated_time': datetime.timestamp(project['updated_time']),
      'last_run': datetime.timestamp(project['last_run'])
    }
    for project in user['projects']
  ] if len(user['projects']) > 0 else []
  # Add project to DB
  return jsonify({
    'message': 'Add projects success !',
    'data': list_project_user,
    'project_add_err': message_res
  })

@project_routes.route('/', methods=['DELETE'])
@token_required
def delete_project(*arg, **kwargs):
  id_project = request.args.get('id')
  logging.warning(f"Project param is {id_project}")
  user = kwargs['user_info']
  deleted_project = None
  try:
    for prj in user['projects']:
      print(prj.id)
      if str(prj.id) == id_project:
        deleted_project = prj
        break
    if not deleted_project:
      return jsonify({
        'message': 'Not found project'
      }), 403
    User.objects(id=user['id']).update_one(pull__projects=deleted_project)
    Project.objects(id=id_project).delete()
    return jsonify({
      'message': 'Delete projects success !'
    })
  except Exception as e:
    logging.error("Have error API delete Project !")
    logging.error(e)
    return jsonify({
      'message': 'Delete project error !'
    }), 400
