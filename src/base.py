from facebook_creds import  facebook_creds, update_token, is_token_expired
from instagram_feed import get_feed
from get_username import get_username
from csv_parser import user_csv_output, read_json, media_csv_output
from image_storage import retrieve_media_url, retrieve_user_profile_url
from check_folder_exists import checar_pasta
from pathlib import Path
import json


def metadata():
    dic = {}
    dic['json_filename'] = 'universities_feed.json'
    dic['users_filename'] = 'usuarios.csv'
    dic['csv_folder'] = Path('pub')
    dic['images_folder'] = Path('images')
    return dic

def folder_checker(metadata):
    checar_pasta(metadata['csv_folder'])
    checar_pasta(metadata['images_folder'])

def token_status(creds):
    if is_token_expired(creds) == False:
        print('Token aceito')
        return update_token(creds)
    return 'O input_token informado está expirado. Você precisa adicionar um input_token válido no arquivo creds_params.json'

def instagram_metadata_download(metadata, creds):
    token_status(creds)
    folder_checker(metadata)
    response_list = []
    for username in get_username(metadata['users_filename']):
        response_list.append(get_feed(username, creds))
        retrieve_media_url(response_list[-1], metadata['images_folder'])
        retrieve_user_profile_url(response_list[-1], metadata['images_folder'])

    with open(metadata['json_filename'], 'w') as f:
        f.write(json.dumps(response_list, indent=5))

def csv_output(metadata):
    json_file = read_json(metadata['json_filename'])
    user_csv_output(json_file, metadata['csv_folder'])
    media_csv_output(json_file, metadata['csv_folder'])
