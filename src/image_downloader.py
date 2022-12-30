import requests
import logging
import pickle
import os
from moviepy.editor import VideoFileClip

def download_media(media: dict, image_folder: str, video_folder: str) -> None:
    """
    Baixa a mídia (imagem ou vídeo) especificada e salva na pasta de destino.
    Se for um vídeo, também gera e salva uma thumbnail na pasta de imagens.
    Args:
        media: Dicionário com os dados da mídia a ser baixada.
        image_folder: Pasta de destino para imagens.
        video_folder: Pasta de destino para vídeos.
    """
    # Verifica se o mídia é uma imagem ou um vídeo
    try:
        if media['media_type'] in ['IMAGE', 'CAROUSEL_ALBUM']:
            folder = image_folder
            file_extension = 'jpg'
        elif media['media_type'] == 'VIDEO':
            folder = video_folder
            file_extension = 'mp4'
        else:
            return

        # Verifica se o arquivo já existe na pasta de destino
        file_path = f'{folder}/{media["id"]}.{file_extension}'
        if os.path.exists(file_path):
            logging.debug(f'A mídia {media["id"]}.{file_extension} já existe, download não necessário')
            return

        # Faz o download da mídia e salva na pasta de destino
        response = requests.get(media['media_url'])
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
