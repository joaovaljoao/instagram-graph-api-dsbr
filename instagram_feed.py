from facebook_creds import facebook_creds, long_lived_token
import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.DEBUG)

s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))


def get_feed(nome_usuario, creds_params):
    
    media_params = 'media_url,comments_count,like_count,caption,media_type,permalink,timestamp,username'

    user_params = 'username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media'

    params = (
    ('fields', 'business_discovery.username(' + nome_usuario + '){' + user_params + '{' + media_params + '}}'),
    ('access_token', long_lived_token(creds_params)['access_token'])
)

    response = requests.get(creds_params['endpoint'] + creds_params['facebook_id'], params=params).json()
    
    return response