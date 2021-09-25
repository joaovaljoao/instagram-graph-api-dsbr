#!/usr/bin/python3
from facebook_creds import  facebook_creds, update_token
from instagram_feed import get_feed
from get_username import get_username
from csv_parser import user_csv_output, read_json, media_csv_output
from image_storage import retrieve_media_url, retrieve_user_profile_url
from check_folder_exists import checar_pasta
from datetime import datetime
import json
from pathlib import Path

json_filename = 'universities_feed.json'
users_filename = 'usuarios.csv'
csv_folder = Path('pub')
images_folder = Path('images')

checar_pasta(csv_folder)
checar_pasta(images_folder)

facebook_creds = facebook_creds()
update_token(facebook_creds)

inicio_download = datetime.now()

response_list = []
for username in get_username(users_filename):
    response_list.append(get_feed(username, facebook_creds))
    retrieve_media_url(response_list[-1], images_folder)
    retrieve_user_profile_url(response_list[-1], images_folder)


with open(json_filename, 'w') as f:
    f.write(json.dumps(response_list, indent=5))
fim = datetime.now()
print(f'----- Download dos dados foi realizado em {fim - inicio_download} -----')


json_file = read_json(json_filename)

user_csv_output(json_file, csv_folder)

media_csv_output(json_file, csv_folder)