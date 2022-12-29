import sys, os
import argparse
import pandas as pd
from business_data import BusinessData
from image_downloader import InstagramImageDownloader
from image_resizer import ImageResizer

# Specify the fields to retrieve
FIELDS = "{username,website,name,ig_id,id,profile_picture_url,\
        biography,follows_count,followers_count,media_count,\
        media{media_url,comments_count, like_count,caption,media_type,permalink,timestamp,username}}"


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

    # Pega o nome do arquivo e carrega os dados em uma lista.
    filename_prefix=file_name.split('.')[0]
    usernames = pd.read_csv('usernames/' + file_name, sep=';')['username'].tolist()


    # Create the BusinessData instance
    business_data = BusinessData()

    # Create an InstagramImageDownloader instance
    downloader = InstagramImageDownloader()

    # TODO: Apagar apenas depois que o downlaod via API tenha sucesso. Mover para uma 
    #       pasta temporária antes.
    if os.path.exists('pub/'+filename_prefix+'_media_data.csv') and os.path.exists('pub/'+filename_prefix+'_user_data.csv'):
        os.unlink('pub/'+filename_prefix+'_media_data.csv')
        os.unlink('pub/'+filename_prefix+'_user_data.csv')

    # Iterate over the list of usernames
    for username in usernames: # Limitado a 2 para não sobrecarregar a API, Mudar na produção
        # Call the get_business_data method
        response = business_data.get_business_data(username, FIELDS)
        # Save the data to CSV files
        business_data.save_to_csv(response, filename_prefix)
        downloader.download_images(response)
        resizer = ImageResizer('pub/'+filename_prefix+'_media_data.csv')
        resizer.process_directory('pub/images')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', default='small.csv')
    args = parser.parse_args()
    run(args.file_name)