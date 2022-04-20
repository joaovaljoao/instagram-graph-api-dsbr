import requests
import json
from datetime import datetime, timedelta

class Facebook:

    def __init__(self) -> None:
    
        self.app_params = json.load(open('input/creds_params.json'))
        self.user_id = self.app_params['facebook_id']
        self.endpoint = self.app_params['endpoint']
        self.grant_type = self.app_params['grant_type']
        self.client_secret = self.app_params['client_secret']
        self.client_id = self.app_params['client_id']
        self.input_token = self.app_params['input_token']
        self.graph_domain = self.app_params['graph_domain']

    def long_lived_token(self) -> dict:
        
        params = (
            ('grant_type', self.grant_type),
            ('client_secret', self.client_secret),
            ('client_id', self.client_id),
            ('fb_exchange_token', self.input_token),
        )

        response = requests.get(self.endpoint + 'oauth/access_token', params = params)
        
        return response.json()

    def debug_token(self) -> dict:
        
        params = (
        (' input_token', self.input_token),
        (' access_token', self.access_token),
        )

        response = requests.get(self.graph_domain + 'debug_token', params=params).json()['data']

        return response

    def is_token_expiring(self) -> bool:
            
            token_expires_in = self.debug_token()['expires_at']
            token_expires_in = datetime.fromtimestamp(token_expires_in)
            update_in = token_expires_in - timedelta(days=7)
            now = datetime.now()
            return update_in < now
