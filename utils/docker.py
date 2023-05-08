import docker
import logging
import re
import datetime
import pytz

tz = pytz.timezone('Asia/Ho_Chi_Minh')

def create_container(project_id, twitter_url, email, table_id='canvas-figure-378911.twitter_crawl.tweet'):
  logging.warning("Creating client docker...")
  client_docker = docker.from_env()
  logging.warning("Start create container...")
  project_name = re.search('(?<=\/\/twitter.com\/)([a-zA-Z0-9]*)', twitter_url).group()
  client_docker.containers.run(
    'crawl_app',
    f'--project_url {twitter_url} --table_id {table_id} --project_id {project_id} --email {email}',
    detach=True,
    volumes={'/home/chudang98hn/cert/': {'bind': '/app/cert/', 'mode': 'ro'}},
    network='flaskserver_backend'
  )
  logging.warning("Created container !")
  client_docker.close()
  logging.warning("Closed client docker !")