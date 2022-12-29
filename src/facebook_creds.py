import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

class Facebook:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Set object attributes from environment variables
        self.input_token = os.getenv('INPUT_TOKEN')
        self.long_lived_token = os.getenv('LONG_LIVED_TOKEN')
        self.grant_type = os.getenv('GRANT_TYPE')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.client_id = os.getenv('CLIENT_ID')
        self.graph_domain = os.getenv('GRAPH_DOMAIN')
        self.version = os.getenv('VERSION')
        self.facebook_id = os.getenv('FACEBOOK_ID')
        self.endpoint = f"{self.graph_domain}{self.version}/{self.facebook_id}"

    def refresh_long_lived_token(self):
        # Make request to Facebook Graph API to exchange INPUT_TOKEN for long-lived token
        params = (
            ('grant_type', self.grant_type),
            ('client_secret', self.client_secret),
            ('client_id', self.client_id),
            ('fb_exchange_token', self.input_token),
        )
        response = requests.get(f"{self.graph_domain}{self.version}/oauth/access_token", params = params)
        long_lived_token = response.json()['access_token']
        expires_in = response.json()['expires_in']

        # Update LONG_LIVED_TOKEN and EXPIRES_IN variables in .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        with open('.env', 'w') as f:
            for line in lines:
                if line.startswith('LONG_LIVED_TOKEN'):
                    f.write('LONG_LIVED_TOKEN=' + long_lived_token + '\n')
                elif line.startswith('EXPIRES_IN'):
                    f.write('EXPIRES_IN=' + expires_in + '\n')
                else:
                    f.write(line)

        # Load updated environment variables from .env file
        load_dotenv()
        
        # Update LONG_LIVED_TOKEN attribute of object
        self.long_lived_token = long_lived_token
            
        return long_lived_token

    def debug_token(self, token):
        params = (
            ('input_token', token),
            ('access_token', self.client_id + '|' + self.client_secret),
        )

        response = requests.get(f"{self.graph_domain}{self.version}/debug_token", params=params).json()

        return response

    def is_token_expiring(self, expiration_threshold_seconds=604800):
        # Check if LONG_LIVED_TOKEN is set in environment
        if 'LONG_LIVED_TOKEN' in os.environ:
            # Use LONG_LIVED_TOKEN
            token = os.environ['LONG_LIVED_TOKEN']
        else:
            # Use INPUT_TOKEN
            token = self.input_token

        # Get expiration time of token
        token_info = self.debug_token(token)['data']
        expiration_time = datetime.fromtimestamp(token_info['expires_at'])

        # Compare expiration time to current time and expiration threshold
        now = datetime.now()
        expiration_threshold = timedelta(seconds=expiration_threshold_seconds)
        if expiration_time < now + expiration_threshold:
            # Refresh token
            self.refresh_long_lived_token()
