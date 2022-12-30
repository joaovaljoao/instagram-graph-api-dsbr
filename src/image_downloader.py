import os
import requests
import logging
import pickle
import configparser
from moviepy.editor import VideoFileClip

config = configparser.ConfigParser()
config.read('config.ini')
image_folder = config['STRUCTURE']['IMAGE_FOLDER']
video_folder = config['STRUCTURE']['VIDEO_FOLDER']

def download_media(media: dict) -> None:
    """
    Baixa a mídia (imagem ou vídeo) especificada e salva na pasta de destino.
    Se for um vídeo, também gera e salva uma thumbnail na pasta de imagens.
    Args:
        media: Dicionário com os dados da mídia a ser baixada.
    """
    # Verifica se o mídia é uma imagem ou um vídeo
    try:
        if media.get('media_type', None) in ['IMAGE', 'CAROUSEL_ALBUM']:
            folder = image_folder
            file_extension = 'jpg'
        elif media.get('media_type', None) == 'VIDEO':
            folder = video_folder
            file_extension = 'mp4'
        else:
            logging.debug(f'Erro: Tipo de midia desconhecido - media: {media.get("media_type", "sem media_type em media")}')
            return

        # Verifica se o arquivo já existe na pasta de destino
        file_path = f'{folder}/{media.get("id", "0000")}.{file_extension}'
        if os.path.exists(file_path):
            logging.debug(f'A mídia {media.get("id", "000")}.{file_extension} já existe, download não necessário')
            return

        # Faz o download da mídia e salva na pasta de destino
        response = requests.get(media.get('media_url', None))
        open(file_path, 'wb').write(response.content)

        # Se for um vídeo, gera e salva o thumbnail na pasta de imagens
        if media['media_type'] == 'VIDEO':
            clip = VideoFileClip(file_path)
            thumbnail_path = f'{image_folder}/{media["id"]}.jpg'
            clip.save_frame(thumbnail_path, t=0.5)

        logging.debug(f'Baixou {media["id"]}.{file_extension}')
        with open(f'logging/pickle/{media["id"]}_image_download.pickle', 'wb') as handle:
            pickle.dump(response, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        logging.debug(f'Erro: {e}')
