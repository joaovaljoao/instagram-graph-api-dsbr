import os
from PIL import Image
import csv
import logging

def get_users_data(csv_file_name: str) -> list:
    """
    Extrai os dados de media do usuário de um arquivo CSV e retorna uma lista de IDs. 
    """
    user_data = []
    try:
        with open(csv_file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                user_data.append(row[0])
        
        # Remove o primeiro elemento (o cabeçalho) e qualquer elemento vazio
        user_data = [x for x in user_data[1:] if x]
    except Exception as e:
        logging.error(f'Error reading CSV file {csv_file_name}: {e}')
        return None

    return user_data

def resize_image(image_path: str) -> None:
    """
    Altera o tamanho de uma imagem dado o caminho para a mesma.
     * Imagens maiores que 1920x1080 são redimensionadas para 1920x1080.
     * Imagens menores que 640x480 são redimensionadas para 640x480.
    A nova imagem é salva no lugar da anterior (mesmo caminho e nome).
    """
    # Verifica se o arquivo já existe
    if os.path.exists(image_path):
        logging.debug(f'{image_path} já existe, resize não necessário')
        return
    try:
        with Image.open(image_path) as im:
            if im.width // 3 > 1920 or im.height // 3 > 1080:
                im = im.resize((1920, 1080))
            elif im.width // 3 < 640 or im.height // 3 < 480:
                im = im.resize((640, 480))
            else:
                im = im.resize((im.width // 3, im.height // 3))
            im.save(image_path)
        logging.debug(f'Resized image {image_path}')
    except Exception as e:
        logging.error(f'Error resizing image {image_path}: {e}')


def process_directory(directory_path: str, user_data: list) -> None:
    """
    Itera sobre todos os arquivos JPEG em um diretório e redimensiona as imagens
    caso ela seja de um id da lista de mídias.
    """
    for filename in os.listdir(directory_path):
        if not filename.endswith('.jpg'):
            continue
        user_id = filename.split('.')[0]
        if user_id in user_data:
            image_path = f'{directory_path}/{filename}'
            resize_image(image_path)
