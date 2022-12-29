import os
import logging
import pickle
import time
import requests
import pandas as pd
import dotenv

# Load the environment variables
dotenv.load_dotenv()

class BusinessData:
    def __init__(self):
        self.input_token = os.getenv('INPUT_TOKEN')
        self.endpoint = os.getenv('GRAPH_DOMAIN') + os.getenv('VERSION') + "/" + os.getenv('FACEBOOK_ID')

    def get_business_data(self, username: str, fields: str) -> dict:
        params = {
            'fields': f'business_discovery.username({username})' + fields,
            'access_token': self.input_token,
        }
        timestamp = time.time()

        try:
            # Make the GET request
            response = requests.get(self.endpoint, params=params)

            # Check the status code
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


    def save_to_csv(self, data: dict, filename_prefix: str) -> None:
        # Extract the data for the user and the media
        user_data = {k: v for k, v in data['business_discovery'].items() if k != 'media'}
        media_data = [{**{'id': data['business_discovery']['id']}, **item} for item in data['business_discovery']['media']['data']]

        # Create the pandas DataFrames
        df_user = pd.DataFrame(user_data, index=[0])
        df_media = pd.DataFrame(media_data)

        # Save the DataFrames to CSV files
        df_user.to_csv('pub/'+filename_prefix+'_user_data.csv', index=False, sep=';', encoding='utf-8-sig', mode='a', header=not os.path.exists('pub/'+filename_prefix+'_user_data.csv'))
        df_media.to_csv('pub/'+filename_prefix+'_media_data.csv', index=False, sep=';', encoding='utf-8-sig', mode='a', header=not os.path.exists('pub/'+filename_prefix+'_media_data.csv'))

def loggin_setup():
    # create logging folder if it doesn't exist
    if not os.path.exists('logging'):
        os.makedirs('logging')

    # create pickle folder if it doesn't exist in the logging directory
    if not os.path.exists('logging/pickle'):
        os.makedirs('logging/pickle')

    # Configure logging
    logging.basicConfig(filename='logging/app.log', filemode='w', format='%(levelname)s - %(message)s', level=logging.DEBUG)

