from facebook_creds import Facebook as fb
import requests


def get_feed(nome_usuario):
    
    media_params = 'media_url,comments_count,like_count,caption,media_type,permalink,timestamp,username'

    user_params = 'username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media'

    params = (
    ('fields', 'business_discovery.username(' + nome_usuario + '){' + user_params + '{' + media_params + '}}'),
    ('access_token', fb().long_lived_token()['access_token'])
)

    response = requests.get(fb().app_params['endpoint'] + fb().app_params['facebook_id'], params=params).json()
    
    return response