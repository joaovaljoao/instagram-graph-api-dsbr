import os, csv
import logging
from PIL import Image

def extract_user_data(cv_file_name: str) -> list:
    '''
    Extrai os dados do usuário de um arquivo CSV e retorna uma lista de IDs. 
    '''
    user_data = []
    with open(cv_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            user_data.append(row[0])
    
    # Remove o primeiro elemento (o cabeçalho) e qualquer elemento vazio
    user_data = [x for x in user_data[1:] if x]

    return user_data

def resize_image(image_path: str) -> None:
    '''
    Altera o tamanho de uma imagem dado o caminho para a mesma.
     * Imagens maiores que 1920x1080 são redimensionadas para 1920x1080.
     * Imagens menores que 640x480 são redimensionadas para 640x480.
    A nova imagem é salva no lugar da anterior (mesmo caminho e nome).
    Retorna verdadeiro caso a operação seja bem sucedida, falso caso contrário.
    '''
    try:
        with Image.open(image_path) as im:
            if im.width // 3 > 1920 or im.height // 3 > 1080:
                im = im.resize((1920, 1080))
            elif im.width // 3 < 640 or im.height // 3 < 480:
                im = im.resize((640, 480))
            else:
                im = im.resize((im.width // 3, im.height // 3))
            im.save(image_path)
        logging.info(f'Resized image {image_path}')
    except Exception as e:
        logging.error(f'Error resizing image {image_path}: {e}')
    
def process_directory(directory_path: str, user_data: list) -> None:
    '''
    Itera sobre todos os arquivos JPEG em um diretório e redimensiona as imagens
    caso ela seja de um id da lista de usuários.
    '''
    for filename in os.listdir(directory_path):
        if not filename.endswith('.jpg'):
            continue
        user_id = filename.split('.')[0]
        if user_id in user_data:
            resize_image(os.path.join(directory_path, filename))
