import requests
import os
import requests


def do_request():
    token_url = 'https://graph.facebook.com/oauth/access_token'
    params = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'fb_exchange_token',
        'fb_exchange_token': 'EAAlVCHCZA7rQBACKBHwbH6G0CLg2CpZC4QgTjfW2xIhP0AzZC50dChaaQkwCYCKV7k8KFZAkHifpZBaq0WZBkNt7P5pJBZCdjnJ1iNxa5GZAPPrZCIfUbIIfI4jyuyMq7pWRZCSDXPgdq1MfIr4M3wbxRysBg5lQdZCbqcE0ZBPDYKo1fYmGZAVMTZCP5HwQwFQTJY33bBQZC9DjdMUxAZDZD',
    }
    r = requests.get(token_url, params=params)

    if r.status_code == 200:
        response = r.json() 
        long_lived_token = response['access_token']
        print(long_lived_token)

    else:
        print(f'Error {r.status_code}: {r.text}')

    # save token to .env file
    with open('.env', 'a') as f:
        f.write(f'LONG_LIVED_TOKEN={long_lived_token}')