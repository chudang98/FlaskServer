from mongoengine import *
import datetime

class Project(Document):
  meta = {'collection': 'project'}
  link = StringField(required=True, unique=True)
  project_name = StringField(required=True, unique=True) # Detect from link `split("https://twitter.com/", 1)[1]`
  updated_time = DateTimeField(default=datetime.datetime.utcnow)
