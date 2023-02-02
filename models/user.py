from mongoengine import *
import datetime

class User(Document):
  meta = {'collection': 'user'}
  username = StringField(required=True, unique=True)
  email = StringField(required=True)
  password = StringField(required=True)
  project = ListField()
  updated_time = DateTimeField(default=datetime.datetime.utcnow)
