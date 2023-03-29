import docker
import logging

def create_container(project_id, twitter_url, table_id=''):
  logging.warning("Creating client docker...")
  client_docker = docker.from_env()
  logging.warning("Start create container...")
  client_docker.containers.run(
    'test_app',
    f'--project_url {twitter_url} --table_id {table_id}',
    detach=True
  )
  logging.warning("Created container !")
  client_docker.close()
  logging.warning("Closed client docker !")