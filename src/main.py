import  os
import argparse
import configparser
import pandas as pd
import business_data
from image_downloader import download_media
from imager import process_directory
from facebook_creds import Facebook

config = configparser.ConfigParser()
config.read('config.ini')
FIELDS = config['INSTAGRAM_API']['FIELDS']

def run(file_name: str) -> None:
    '''
    Função principal do programa que busca pela API do Instagram os dados 
    listados em FIELDS das contas listadas no arquivo de entrada (file_name).
    
    O arquivo de entrada é um csv dentro da pasta usernames e deve ter
    as colunas UO;username relativas ao username e ID no Instagram.
    
    Os dados são salvos em arquivos e imagens são baixadas e salvas na pasta PUB
    com nomes de acordo com o arquivo de entrada. TODO: Detalhar como é salvo 
    (local, nomes e etc).
    '''
    business_data.create_folder()
    business_data.loggin_setup()
    # Pega o nome do arquivo e carrega os dados em uma lista.
    filename_prefix=file_name.split('.')[0]
    usernames = pd.read_csv('usernames/' + file_name, sep=';')['username'].tolist()

    # Create a Facebook instance
    fb = Facebook()

    # Check if long-lived token is expiring
    if fb.is_token_expiring(expiration_threshold_seconds=604800):  # 7 days in seconds
        fb.refresh_long_lived_token()

    if os.path.exists('pub/'+filename_prefix+'_media_data.csv') and os.path.exists('pub/'+filename_prefix+'_user_data.csv'):
        os.unlink('pub/'+filename_prefix+'_media_data.csv')
        os.unlink('pub/'+filename_prefix+'_user_data.csv')

    # Iterate over the list of usernames
    for username in usernames: # Limitado a 2 para não sobrecarregar a API, Mudar na produção
        # Call the get_business_data method
        response = business_data.get_business_data(username, FIELDS)
        # Save the data to CSV files
        business_data.save_to_csv(response, filename_prefix)
        data = response['business_discovery']['media']['data']
        # Download the media
        for media in data:
            download_media(media)
        # get all jpg files in the directory and get id
        user_data = [x.split('.')[0] for x in os.listdir('pub/images') if x.endswith('.jpg')]
        process_directory('pub/images', user_data, width=640, height=480) # Agora você pode determinar as dimensões da imagem no main.py.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', default='small.csv')
    args = parser.parse_args()
    run(args.file_name)