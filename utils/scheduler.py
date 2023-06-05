from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import pymongo
import logging
import datetime
from utils.docker import create_container
from utils.twitter_api import get_profile_twitter

MONGODB_URL = "mongodb://admin:password@mongodb:27017/twitter_crawler?authSource=admin&retryWrites=true&w=majority"
MONGODB_DB = "twitter_crawler"
MONGODB_PROJECT_COLLECTION = "project"

schedule_idx = {
  '1 hour': 1,
  '2 hours': 2,
  '6 hours': 3,
  '1 day': 4,
  '2 day': 5,
  '3 day': 6,
  '1 week': 7,
  '2 weeks': 8,
  '3 weeks': 9,
  '1 month': 10
}

schedule_convert = {
  '1 hour': {'hours': 1},
  '2 hours': {'hours': 2},
  '6 hours': {'hours': 6},
  '1 day': {'days': 1},
  '2 day': {'days': 2},
  '3 day': {'days': 3},
  '1 week': {'weeks': 1},
  '2 weeks': {'weeks': 2},
  '3 weeks': {'weeks': 3},
  '1 month': {'months': 1}
}

schedule_timedelta = {
  '1 hour': datetime.timedelta(hours=1),
  '2 hours': datetime.timedelta(hours=2),
  '6 hours': datetime.timedelta(hours=6),
  '1 day': datetime.timedelta(days=1),
  '2 day': datetime.timedelta(days=2),
  '3 day': datetime.timedelta(days=3),
  '1 week': datetime.timedelta(weeks=1),
  '2 weeks': datetime.timedelta(weeks=2),
  '3 weeks': datetime.timedelta(weeks=3),
  '1 month': datetime.timedelta(days=30)
}

def init_schedule_crawl():
  logging.warning("Start init schedule job...")
  client = pymongo.MongoClient(MONGODB_URL)
  logging.warning("Created client MongoDB for schedule job.s")
  jobstores = {
    'mongo': MongoDBJobStore(client=client, collection="schedulejob"),
    'default': MongoDBJobStore(client=client, collection="schedulejob")

  }
  executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(2)
  }
  job_defaults = {
    'coalesce': False,
    'max_instances': 1
  }

  db = client[MONGODB_DB]
  collection = db[MONGODB_PROJECT_COLLECTION]
  all_projects = collection.find()
  schedule_job = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults
  )
  schedule_job.start()
  all_jobs = schedule_job.get_jobs()
  if len(all_jobs) > 0:
    logging.warning("All job had schedule! Done!")
    return schedule_job
  else:
    logging.warning("Start init job...")

  projects = []
  project_names = []
  for project in all_projects:
    if project['project_name'] not in project_names:
      logging.warning(f"Adding new job for project {project['link']} with name project is {project['project_name']}...")
      projects.append({
        'project_name': project['project_name'],
        'project_id': project['id'],
        'frequence': project['frequency'],
        'link': project['link']
      })
      project_names.append(project['project_name'])

    else:
      for i in projects:
        if i['project_name'] == project['project_name']:
          if schedule_idx[i['frequency']] > schedule_idx[project['frequency']]:
            i['frequency'] = project['frequency']
          break

  for project in projects:
    interval_time = project['frequency']
    # TODO: Check job
    profile = get_profile_twitter(project['link'])
    if 'data' in profile.json():
      schedule_job.add_job(create_container,
                           'interval',
                           args=[project['project_id'], project['link'], 'None'],
                           name=project['project_name'],
                           jobstore='mongo',
                           start_date=datetime.datetime.now(),
                           **schedule_convert[interval_time])
      logging.warning(f"Added project {project['project_name']} with schedule is {project['frequency']}")
    else:
      logging.warning(f"Error when schedule project {project['project_name']} because cannot find project !")
  schedule_job.start()
  logging.warning("Started all job !")
  return schedule_job

def add_schedule_job(scheduler_crawler: BackgroundScheduler, job_new):
  all_jobs = scheduler_crawler.get_jobs()
  for job in all_jobs:
    if job.name == job_new['project']:
      if job.trigger.interval > schedule_timedelta[job_new['frequence']]:
        logging.warning(f"Update job {job.name} with new schedule !")
        scheduler_crawler.reschedule_job(job.id,
                                 trigger='interval',)
      else:
        logging.warning(f"Job {job.name} not need to re-schedule !")
      return
  scheduler_crawler.add_job(create_container,
        trigger='interval',
        args=[job_new['project_id'], job_new['link'], 'None'],
        name=job_new['project_name'],
        jobstore='mongo',
        start_date=datetime.datetime.now() + schedule_timedelta[job_new['frequence']],
        **schedule_convert[job_new['frequence']])
  logging.warning(f"Added new job {job_new['project']}")

def delete_job(scheduler_crawler: BackgroundScheduler, job_name):
  all_jobs = scheduler_crawler.get_jobs()
  for job in all_jobs:
    if job.name == job_name:
      logging.warning(f"Delete job have id {job.id} and name is {job_name}")
      scheduler_crawler.remove_job(job.id)
      return
  pass