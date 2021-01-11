import config

import jwt
import time
import os
import base64


from logzero import logger


import urllib.parse as urlparse
from urllib.parse import urlencode

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

authorization_codes = {}

with open('private.pem', 'rb') as f:
    private_key = f.read()


def verify_client_info(client_id, redirect_url):
    if ( client_id == config.CLIENT_ID and redirect_url in config.REDIRECT_URL ):
        return True
    else:
        return False


def authenticate_user_credentials(username, password):

    if ( username == config.USERNAME and password == config.PASSWORD ):
        return True
    else:
        return False

def process_redirect_url(redirect_url, new_entries):
  # Prepare the redirect URL
  logger.warn("process_redirect_url started")
  logger.warn("--> new_entries: {}".format(new_entries))
  url_parts = list(urlparse.urlparse(redirect_url))
  logger.warn("--> url_parts: {}".format(url_parts))
  queries = dict(urlparse.parse_qsl(url_parts[4]))
  logger.warn("--> queries: {}".format(queries))
  queries.update(new_entries)
  
  url_parts[4] = urlencode(queries)
  logger.warn("--> url_parts[4]: {}".format(url_parts[4]))
  url = urlparse.urlunparse(url_parts)
  logger.warn("--> url: {}".format(url))
  return url

def generate_state_parameter():
  random = os.urandom(256)
  state = base64.b64encode(random)
  return (state)

def generate_access_token():
    payload = {
        # "iss": ISSUER,
        # "exp": time.time() + JWT_LIFE_SPAN,
        "sub": 1234
    }

    access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()

    return access_token