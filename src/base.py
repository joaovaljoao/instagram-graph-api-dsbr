from facebook_creds import  Facebook as fb
from instagram_feed import get_feed
from get_username import get_username
from csv_parser import user_csv_output, read_json, media_csv_output
from image_storage import retrieve_media_url, retrieve_user_profile_url
from support import SuppportFunctions
from pathlib import Path
import json
import sys


def metadata():
    dic = {}
    csv_file = sys.argv[1]
    json_file = csv_file.split('.')[0] + '_feed.json'
    dic['json_filename'] = json_file
    dic['users_filename'] = csv_file
    dic['csv_folder'] = Path('../pub')
    dic['images_folder'] = Path('../images')
    return dic

def folder_checker(metadata):
    SuppportFunctions.create_folder_exists(metadata['csv_folder'])
    SuppportFunctions.create_folder_exists(metadata['images_folder'])

def token_status():
    if fb().is_token_expiring() == False:
        return print('Token aceito')
    return print('O input_token informado está expirando e, portanto, foi atualizado')

def instagram_metadata_download(metadata):
    token_status()
    folder_checker(metadata)
    response_list = []
    for username in get_username(metadata['users_filename'])[0]:
        response_list.append(get_feed(username))
        retrieve_media_url(response_list[-1], metadata['images_folder'])
        retrieve_user_profile_url(response_list[-1], metadata['images_folder'])

    with open(metadata['json_filename'], 'w') as f:
        f.write(json.dumps(response_list, indent=5))

def csv_output(metadata):
    json_file = read_json(metadata['json_filename'])
    user_csv_output(json_file, metadata['csv_folder'])
    media_csv_output(json_file, metadata['csv_folder'])
