import requests
import json
from datetime import datetime, timedelta
from support import SuppportFunctions

class Facebook:

    def __init__(self) -> None:
    
        self.app_params = json.load(open('creds_params.json'))

    def long_lived_token(self):
        
        params = (
            ('grant_type', self.app_params['grant_type']),
            ('client_secret', self.app_params['client_secret']),
            ('client_id', self.app_params['client_id']),
            ('fb_exchange_token', self.app_params['input_token']),
        )

        response = requests.get(self.app_params['endpoint'] + 'oauth/access_token', params = params)
        
        return response.json()

    def debug_token(self):
        
        params = (
        (' input_token', self.app_params['input_token']),
        (' access_token', self.app_params['access_token']),
        )

        response = requests.get(self.app_params['graph_domain'] + 'debug_token', params=params).json()['data']

        return response

    def is_token_expiring(self):
        expiration_date = self.app_params['expires_at']
        if (datetime.now() + timedelta(days=7)) >= datetime.fromisoformat(expiration_date):
            self.app_params['input_token'] = self.long_lived_token()['access_token']
            self.app_params['expires_at'] = SuppportFunctions.epoch_to_dt(self.long_lived_token()['expires_in'])
            return True
        return False