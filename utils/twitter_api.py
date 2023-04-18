import logging

# import pytz
# import os
# import sys
import time
import requests
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + '/../')
time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAD%2BUkgEAAAAAxuCobQH%2FAcqOzlk6MitTc3vy9no%3DjtTDVRwOEtPhdJEVP1NVIgCtrTIJGAFVDkv7z3UnfV6mvKOlUG'
header_token = {"Authorization": f"Bearer {bearer_token}"}

def __call_api(api_url, req_params):
  for _ in range(5):
    try:
      response_api = requests.get(
        api_url,
        headers=header_token,
        params=req_params
      )
      if response_api.json().get('status', 0) == 429:
        logging.ERROR("Error limit request Twitter API !!!")
        raise Exception("Limit request Twitter API !!!!!")
    except Exception as e:
      logging.error(f'Error when call API !!!!')
      if response_api.json().get('status', 0) == 429:
        logging.warning('Sleeping 10 minutes...')
        time.sleep(600)
        continue
      else:
        logging.error("Error Tweeter API cannot handle !")
        logging.error(e)
        break
    else:
      logging.warning('Call request success.')
      return response_api

def get_profile_twitter(username):
  api_url = f'https://api.twitter.com/2/users/by/username/{username}'
  query_param = {
    "user.fields": "id,location,name,protected,url,username,verified,withheld"
  }
  response_api = __call_api(api_url, query_param)
  return response_api