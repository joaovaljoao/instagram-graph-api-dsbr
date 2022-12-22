import pickle
import logging
import os
import requests

class InstagramImageDownloader:
    def __init__(self):
        pass

    def download_images(self, response):
        # Iterate over the media items in the response
        for item in response['business_discovery']['media']['data']:
            # Skip media items that are not images
            if item['media_type'] == 'VIDEO':
                continue
            else:
                media_url = item['media_url']

            # Create an ImageDownloader instance to download the image
            image_downloader = ImageDownloader(media_url, 'images')
            try:
                image_downloader.download_image(item['id'])
            except Exception as e:
                logging.debug(f'Error: {e}')
                with open(f'logging/pickle/{item["id"]}_image_download.pickle', 'wb') as handle:
                    pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)
                continue


class ImageDownloader:
    def __init__(self, image_url, folder_path):
        self.image_url = image_url
        self.folder_path = folder_path

    def download_image(self, file_name):
        # Check if the folder path exists, and create it if it doesn't
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # Download the image and save it to the specified folder
        response = requests.get(self.image_url)
        open(f'{self.folder_path}/{file_name}.jpg', 'wb').write(response.content)

# create logging folder if it doesn't exist
if not os.path.exists('logging'):
    os.makedirs('logging')

# create pickle folder if it doesn't exist in the logging directory
if not os.path.exists('logging/pickle'):
    os.makedirs('logging/pickle')

# create images folder if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Configure logging
logging.basicConfig(filename='logging/app.log', filemode='w', format='%(levelname)s - %(message)s', level=logging.DEBUG)