from flask import Flask, redirect, render_template, request
from auth import (authenticate_user_credentials, generate_access_token,  
                  verify_client_info, JWT_LIFE_SPAN, 
                  generate_state_parameter, process_redirect_url)

from flask_wtf.csrf import CSRFProtect
                  
import json

import secrets

from logzero import logger


import config

api = Flask(__name__)


@api.route('/')
def hello():
    return "Hello World from Flask"




@api.route('/auth')
def auth():

    client_id = config.CLIENT_ID

    redirect_url = config.REDIRECT_URL[0]

    response_type = config.RESPONSE_TYPE

    state = secrets.token_urlsafe(16)

    return render_template('login.html',
                            client_id = client_id,
                            redirect_url = redirect_url,
                            response_type = response_type,
                            state = state)



@api.route('/signin', methods = ['POST'])
def signin():
    username = request.form.get('username')
    logger.info("--> username: {}".format(username))

    password = request.form.get('password')
    logger.info("--> password: {}".format(password))

    client_id = request.form.get('client_id')
    logger.info("--> client_id: {}".format(client_id))


    redirect_url = request.form.get('redirect_url')
    logger.info("--> redirect_url: {}".format(redirect_url))

    response_type = request.form.get('response_type')
    logger.info("--> response_type: {}".format(response_type))

    state = request.form.get('state')
    logger.info("--> state: {}".format(state))



    if None in [username, password, client_id, redirect_url]:
        return json.dumps({
            "error": "invalid_request"
            }), 400

    if not verify_client_info(client_id, redirect_url):
        return json.dumps({
            "error": "invalid_client"
            }) 

    if not authenticate_user_credentials(username, password):
        return json.dumps({
            'error': 'access_denied'
            }), 401


    access_token = generate_access_token()

    url = '{}#state={}&access_token={}&token_type=Bearer'.format(redirect_url, state, access_token)

    return redirect(url, code=303)