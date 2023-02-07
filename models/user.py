from mongoengine import *
import datetime
from models.projects import Project

class User(Document):
  meta = {'collection': 'user'}
  username = StringField(required=True, unique=True)
  email = StringField(required=True, unique=True)
  password = StringField(required=True)
  projects = ListField(ReferenceField(Project, dbref=True))
  created_time = DateTimeField(default=datetime.datetime.utcnow)
  updated_time = DateTimeField(default=datetime.datetime.utcnow)

  def save(self, *args, **kwargs):
    if not self.created_time:
      self.created_time = datetime.datetime.now()
    self.updated_time = datetime.datetime.now()
    return super(User, self).save(*args, **kwargs)
