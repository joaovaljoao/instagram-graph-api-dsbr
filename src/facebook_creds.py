import requests
import json
from datetime import datetime


def facebook_creds():
    return json.load(open('creds_params.json'))

def long_lived_token(facebook_creds):
    
    params = (
        ('grant_type', facebook_creds['grant_type']),
        ('client_secret', facebook_creds['client_secret']),
        ('client_id', facebook_creds['client_id']),
        ('fb_exchange_token', facebook_creds['input_token']),
    )

    response = requests.get(facebook_creds['endpoint'] + 'oauth/access_token', params=params)
    
    return response.json()

def update_token(facebook_creds):
    facebook_creds['input_token'] = long_lived_token(facebook_creds)['access_token']
    with open('creds_params.json', 'w') as f:
        f.write(json.dumps(facebook_creds, indent=5))


def debug_token(facebook_creds):
    
    params = (
    (' input_token', facebook_creds['input_token']),
    (' access_token', facebook_creds['access_token']),
    )

    response = requests.get( facebook_creds['graph_domain'] + 'debug_token', params=params).json()['data']
    
    return response

def is_token_expired(facebook_creds):
    debug = debug_token(facebook_creds)
    expiration_date = debug['data_access_expires_at']
    if datetime.utcfromtimestamp(expiration_date) <= datetime.now():
        return True
    return False

