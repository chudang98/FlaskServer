from mongoengine import *
import datetime

class Project(Document):
  meta = {'collection': 'project'}
  link = StringField(required=True)
  project_name = StringField(required=True) # Detect from link `split("https://twitter.com/", 1)[1]`
  active = BooleanField(required=True, default=True)
  frequency = StringField(required=True)
  created_time = DateTimeField(default=datetime.datetime.utcnow)
  updated_time = DateTimeField(default=datetime.datetime.utcnow)

  def save(self, *args, **kwargs):
    if not self.created_time:
      self.created_time = datetime.datetime.now()
    self.updated_time = datetime.datetime.now()
    return super(Project, self).save(*args, **kwargs)
