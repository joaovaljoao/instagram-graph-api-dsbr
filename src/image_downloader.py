import requests
from moviepy.editor import VideoFileClip
import logging
import pickle

def download_media(media, image_folder, video_folder):
    # Check if the media is an image or a video
    try:
        if media['media_type'] in ['IMAGE', 'CAROUSEL_ALBUM']:
            folder = image_folder
            file_extension = 'jpg'
        elif media['media_type'] == 'VIDEO':
            folder = video_folder
            file_extension = 'mp4'
        else:
            return

        # Download the media and save it to the specified folder
        response = requests.get(media['media_url'])
        open(f'{folder}/{media["id"]}.{file_extension}', 'wb').write(response.content)

        # If the media is a video, generate a thumbnail and save it to the image folder
        if media['media_type'] == 'VIDEO':
            clip = VideoFileClip(f'{folder}/{media["id"]}.mp4')
            thumbnail_path = f'{image_folder}/{media["id"]}.jpg'
            clip.save_frame(thumbnail_path, t=0.5)

        logging.debug(f'Downloaded {media["id"]}.{file_extension}')
        with open(f'logging/pickle/{media["id"]}_image_download.pickle', 'wb') as handle:
            pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        logging.debug(f'Error: {e}')
