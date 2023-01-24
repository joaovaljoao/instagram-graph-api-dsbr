import os
from typing import List
from PIL import Image
import logging

def resize_image(image_path: str, width: int, height: int) -> None:
    """
    Redimensiona uma imagem dado o caminho para a mesma para as dimensões especificadas.
    A nova imagem é salva no lugar da anterior (mesmo caminho e nome).
    """
    try:
        with Image.open(image_path) as im:
            # Calcula a proporção de redução de tamanho necessária
            ratio = min(width / im.width, height / im.height)
            new_size = (int(im.width * ratio), int(im.height * ratio))
            im = im.resize(new_size)
            im.save(image_path)
        logging.debug(f'Imagem redimensionada: {image_path}')
    except IOError:
        logging.error(f'Erro ao abrir imagem {image_path}')
    except ValueError:
        logging.error(f'Erro ao redimensionar imagem {image_path}: formato de imagem inválido')


def process_directory(directory_path: str, user_data: List[str], width: int, height: int) -> None:

    """
    Itera sobre todos os arquivos JPEG em um diretório e redimensiona as imagens cujo ID está na lista de dados do usuário.
    """
    resized_images_file = 'logging/resized_images.txt'
    # Criar o arquivo resized_images.txt se ele não existir
    if not os.path.exists(resized_images_file):
        with open(resized_images_file, 'w') as f:
            f.write('')
    # Carrega a lista de IDs de imagens redimensionadas
    with open(resized_images_file, 'r') as f:
        resized_images = set(f.read().split())

    for filename in os.listdir(directory_path):
        base, ext = os.path.splitext(filename)
        if ext != '.jpg':
            continue
        user_id = base
        if user_id in user_data:
            # Checa se a imagem já foi redimensionada
            if user_id in resized_images:
                #logging.debug(f'{filename} ignorado porque já foi redimensionado')
                continue
            # Redimensiona a imagem e adiciona o ID à lista de imagens redimensionadas
            logging.debug(f'{filename} está sendo redimensionado')
            image_path = os.path.join(directory_path, filename)
            resize_image(image_path, width, height)
            resized_images.add(user_id)

    # Salva a lista de imagens redimensionadas atualizada
    with open(resized_images_file, 'w') as f:
        f.write('\n'.join(resized_images))



