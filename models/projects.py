from mongoengine import *
import datetime

class Project(Document):
  meta = {'collection': 'project'}
  link = StringField(required=True, unique=False)
  project_name = StringField(required=True, unique=False) # Detect from link `split("https://twitter.com/", 1)[1]`
  active = BooleanField(required=True, default=True, unique=False)
  status = BooleanField(required=False, default='Not process', unique=False)
  frequency = StringField(required=True, unique=False)
  created_time = DateTimeField(default=datetime.datetime.utcnow, unique=False)
  updated_time = DateTimeField(default=datetime.datetime.utcnow, unique=False)

  def save(self, *args, **kwargs):
    if not self.created_time:
      self.created_time = datetime.datetime.now()
    self.updated_time = datetime.datetime.now()
    return super(Project, self).save(*args, **kwargs)
