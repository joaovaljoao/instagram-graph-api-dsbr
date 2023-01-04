import os
import logging
import pickle
import time
import requests
import pandas as pd
import dotenv

# Load the environment variables
dotenv.load_dotenv()

input_token = os.getenv('LONG_LIVED_TOKEN')
endpoint = os.getenv('GRAPH_DOMAIN') + os.getenv('VERSION') + \
           "/" + os.getenv('FACEBOOK_ID')


def get_business_data(username: str, fields: str) -> dict:
    '''
    Faz um request ao Graph API para obter os dados de um usuário do
    Instagram em formato de dicionário.

    Args:
        username: String com o nome de usuário do Instagram.
        fields: String com os campos que devem ser retornados pelo request.
    '''
    params = {
        'fields': f'business_discovery.username({username})' + '{' + fields + '}}',
        'access_token': input_token,
    }
    timestamp = time.time()

    try:
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            logging.warning(f'{timestamp} - {username} - Error: {response.status_code}')
            with open(f'logging/pickle/{timestamp}_business_data.pickle', 'wb') as handle:
                pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except requests.ConnectionError as e:
        logging.error(f'ConnectionError: {e}')
        return None
    except requests.HTTPError as e:
        logging.error(f'HTTPError: {e}')
        return None
    except Exception as e:
        logging.error(f'Error: {e}')
        return None
    return response.json()


def save_to_csv(data: dict, filename_prefix: str) -> None:
    '''
    Salva os dados de um usuário do Instagram em um arquivo CSV.

    Args:
        data: Dicionário com os dados de um usuário do Instagram.
        filename_prefix: String com o prefixo do nome do arquivo CSV.
    '''
    # Create a list of dictionaries with the desired keys
    desired_keys = ['username', 'website', 'name', 'ig_id', 'id', 'profile_picture_url', 'biography', 'follows_count', 'followers_count', 'media_count']
    user_data_list = [{k: data['business_discovery'].get(k, None) for k in desired_keys}]

    # Extract the media data
    media_data = [{**{'id': data['business_discovery']['id']},
                   **item} for item in data['business_discovery']['media']['data']]

    # Create the pandas DataFrames
    df_user = pd.DataFrame(user_data_list)
    df_media = pd.DataFrame(media_data)
    # Save the DataFrames to CSV files
    df_user.to_csv('pub/'+filename_prefix+'_user_data.csv',
                   index=False, sep=';', encoding='utf-8-sig',
                   mode='a',
                   header=not os.path.exists('pub/'+filename_prefix+'_user_data.csv'))
    df_media.to_csv('pub/'+filename_prefix+'_media_data.csv',
                    index=False, sep=';',
                    encoding='utf-8-sig', mode='a',
                    header=not os.path.exists('pub/'+filename_prefix+'_media_data.csv'))



def loggin_setup():
    '''setup logging'''
    # create logging folder if it doesn't exist
    if not os.path.exists('logging'):
        os.makedirs('logging')
    # create pickle folder if it doesn't exist in the logging directory
    if not os.path.exists('logging/pickle'):
        os.makedirs('logging/pickle')
    logging.basicConfig(filename='logging/app.log',
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)


def create_folder():
    '''create folder if it doesn't exist'''
    if not os.path.exists('pub'):
        os.makedirs('pub')
    if not os.path.exists('pub/videos'):
        os.makedirs('pub/videos')
    if not os.path.exists('pub/images'):
        os.makedirs('pub/images')
