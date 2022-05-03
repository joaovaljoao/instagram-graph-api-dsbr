from facebook_creds import Facebook
import requests

class InstagramGraphApi:

    def __init__(self) -> None:
        self.access_token = Facebook().long_lived_token()['access_token']
        fb = Facebook()
        self.facebook_id = fb.facebook_id
        self.endpoint = fb.endpoint
        self.children = 'media_url,media_type'
        self.media_fields = 'caption,comments_count,id,like_count,media_type,media_url,permalink,timestamp,children{' + self.children + '}'

    def business_discovery(self, username:str, pages=10) -> dict:
        """O método business_discovery() recebe um nome de usuário do Instagram e retorna
            um dicionário com informações sobre o perfil e suas postagens. Os dados são
            paginados e retornados em uma lista de dicionários.

        Args:
            username (str): nome de usuário do perfil do Instagram no qual se deseja obter informações.
            pages (int, optional): Número de páginas que serão retornadas. Cada página retorna 25 itens. Defaults to 10.

        Returns:
            dict: O método retorna um dicionário com as seguintes chaves:
            - id: ID do perfil
            - username: nome de usuário do perfil
            - biography: biografia do perfil
            - media_count: número de posts do perfil
            - follower_count: número de seguidores do perfil
            - following_count: número de seguindo do perfil

        """
        user_params = \
            'username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count,media'

        params = (('fields', 'business_discovery.username(' + username
                + '){' + user_params + '{' + self.media_fields + '}}'),
                ('access_token', self.access_token))

        response = requests.get(self.endpoint + self.facebook_id, params=params)

        #paginate business_discovery
        data = response.json()
        # data = Pagination(data, pages).after(username, user_params)
        
        return data

    def get_hashtag_id(self, hashtag:str) -> str:
        """ Esse método recebe um nome de hashtag e retorna o ID dela.

        Args:
            hashtag (str): nome de hashtag do Instagram.

        Returns:
            str: ID da hashtag.
        """
        params = {
            'user_id': self.facebook_id,
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
            'user_id': self.facebook_id,
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
            'user_id': self.facebook_id,
        }

        response = requests.get(self.endpoint + hashtag_id + '/recent_media', params=params)

        data = response.json()
        # data = Pagination(data, pages).next()
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
        data = self.data['data']
        page = 1
        while page <= self.pages:
            next = self.data['paging']['next'] if 'next' in self.data['paging'] else None
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
            response = requests.get(self.endpoint + self.facebook_id, params=params).json()
            data = self.data['business_discovery']['media']['data'].extend(response['business_discovery']['media']['data'])

            page += 1
        else:
            return data