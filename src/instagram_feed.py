from facebook_creds import Facebook as fb
import requests

class InstagramGraphApi:

    def __init__(self) -> None:

        self.access_token = fb().long_lived_token()['access_token']
        self.user_id = fb().app_params['facebook_id']
        self.endpoint = fb().app_params['endpoint']
        self.children = 'media_url,media_type'
        self.media_fields = 'caption,comments_count,id,like_count,media_type,media_url,permalink,timestamp,children{' + self.children + '}'

    def business_discovery(self, username:str, pages=10) -> dict:

        user_params = \
            'username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media'

        params = (('fields', 'business_discovery.username(' + username
                + '){' + user_params + '{' + self.media_fields + '}}'),
                ('access_token', self.access_token))

        response = requests.get(self.endpoint + self.user_id, params=params)

        #paginate business_discovery
        data = response.json()
        data = Pagination(data, pages).after(username, user_params)
        
        return data

    def get_hashtag_id(self, hashtag:str) -> str:

        params = {
            'user_id': self.user_id,
            'q': hashtag,
            'access_token': self.access_token,
        }
        response = requests.get(self.endpoint + 'ig_hashtag_search', params=params)
        return response.json()['data'][0]['id']
    
    def top_media(self, hashtag:str, pages:int=10) -> dict:

        hashtag_id = self.get_hashtag_id(hashtag)

        params = {
            'fields': self.media_fields,
            'access_token': self.access_token,
            'user_id': self.user_id,
        }

        response = requests.get(self.endpoint + hashtag_id + '/top_media', params=params)

        #paginate response
        data = response.json()
        data = Pagination(data, pages).next()
        return data

    def recent_media(self, hashtag:str, pages:int=10) -> dict:

        hashtag_id = self.get_hashtag_id(hashtag)

        params = {
            'fields': self.media_fields,
            'access_token': self.access_token,
            'user_id': self.user_id,
        }

        response = requests.get(self.endpoint + hashtag_id + '/recent_media', params=params)

        data = response.json()
        data = Pagination(data, pages).next()
        return data
    
    def filter_caption(self, search_term:str, content:dict) -> dict:
        for data in content:
            if search_term.lower().strip() in data['caption'].lower().strip():
                data['search_term'] = search_term
        return content
        
class Pagination(InstagramGraphApi):

    def __init__(self, data:dict, pages:int=10) -> None:
        InstagramGraphApi.__init__(self)
        self.data = data
        self.pages = pages


    def next(self) -> dict:
        next = self.data['paging']['next'] if 'next' in self.data['paging'] else None
        data = self.data['data']
        page = 1
        while page <= self.pages:
            response = requests.get(next).json()
            next = response['paging']['next'] if 'paging' in response else None
            data.extend(response['data'])
            page += 1    
        else:
            return data
    
    def after(self, username:str, user_params:str) -> dict:
        page = 1
        while page <= self.pages:
            after = self.data['business_discovery']['media']['paging']['cursors']['after']
            params = (('fields', 'business_discovery.username(' + username
                    + '){' + user_params + f'.after({after})' + '{' + self.media_fields + '}}'),
                    ('access_token', self.access_token))
            response = requests.get(self.endpoint + self.user_id, params=params).json()
            data = self.data['business_discovery']['media']['data'].extend(response['business_discovery']['media']['data'])

            page += 1
        else:
            return data