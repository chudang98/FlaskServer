import logging

from google.cloud import bigquery
from google.oauth2 import service_account

SA_AUTH = '/app/cert/canvas-figure-bq.json'

def create_client():
  logging.warning("Start create client BigQuery...")
  path_auth = SA_AUTH
  logging.warning("Loading credentials...")
  credentials = service_account.Credentials.from_service_account_file(
    path_auth, scopes=["https://www.googleapis.com/auth/cloud-platform"],
  )
  client = bigquery.Client(credentials=credentials, project=credentials.project_id)
  logging.warning("Created client BigQuery !")
  return client

def query_get_all_user_project(project_id, table='canvas-figure-378911.twitter_crawl.permission'):
  bq_client = create_client()
  query = f"""
    SELECT *
    FROM {table}
    WHERE project_id = '{project_id}'
  """
# query = f"""
#   SELECT *
#   FROM canvas-figure-378911.twitter_crawl.permission
#   WHERE project_id = '1452566468793540610' OR project_id = '1448131826300579841'
# """
  query_job = bq_client.query(query)
  list_user = []
  for result in query_job:
    list_user += result[1]
  bq_client.close()
  return list(dict.fromkeys(list_user))

def add_read_project_id_permission(list_prj_ids, email, table='canvas-figure-378911.twitter_crawl.permission'):
  bq_client = create_client()
  condition_qr = ','.join([f"'{prj_id}'" for prj_id in list_prj_ids])
  # TODO: Check have permission for project_id by 2 step : Query by project_id and check email.
  check_permission_qr = f"""
    SELECT project_id, email
    FROM `{table}`
    WHERE project_id in ({condition_qr})
  """
  logging.warning(f"Query get all project_id permission : {check_permission_qr}")
  existed_permission = bq_client.query(check_permission_qr)
  for project_permistion in existed_permission:
    # TODO: Check email has permisstion for this project_id
    list_emails = project_permistion[1]
    if email not in list_emails:
      query_update = f""""
        UPDATE `{table}`
        SET email = ARRAY_CONCAT(email, ['{email}'])
        WHERE project_id = '{project_permistion[0]}'
      """
      logging.warning(f"Query add email {email} to project_id {project_permistion[0]} : {query_update}")
      bq_client.query(query_update)

# TODO: Add project_id permision for first time save or had been deleted.
  prj_existed = [proj[0] for proj in existed_permission]
  for prj_id in list_prj_ids:
    if prj_id not in prj_existed:
      query = f"""
        INSERT INTO `{table}`(project_id, email)
        VALUES('{prj_id}', ['{email}'])  
      """
      logging.warning(f"""
          Project id {prj_id} is new.
          Query add new project id {prj_id} for email {email}
      """)
      bq_client.query(query)
  bq_client.close()
