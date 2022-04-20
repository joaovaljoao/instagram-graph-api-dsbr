from instagram_feed import InstagramFeed
from csv_parser import user_csv_output, read_json, media_csv_output, get_username
from image_storage import retrieve_media_url, retrieve_user_profile_url
from pathlib import Path
import json
import sys
import errno


def metadata():
    dic = {}
    csv_file = sys.argv[1]
    json_file = csv_file.split('.')[0] + '_feed.json'
    dic['json_filename'] = json_file
    dic['users_filename'] = csv_file
    dic['csv_folder'] = Path('../pub')
    dic['images_folder'] = Path('../images')
    return dic

def touch(folder):
    try:
        Path(folder).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def instagram_metadata_download(metadata):
    touch(metadata['csv_folder'])
    touch(metadata['images_folder'])
    response_list = []
    for username in get_username(metadata['users_filename']):
        response_list.append(InstagramFeed(username).user_feed)
        retrieve_media_url(response_list[-1], metadata['images_folder'])
        retrieve_user_profile_url(response_list[-1], metadata['images_folder'])

    with open(metadata['json_filename'], 'w') as f:
        f.write(json.dumps(response_list, indent=5))

def csv_output(metadata):
    json_file = read_json(metadata['json_filename'])
    user_csv_output(json_file, metadata['csv_folder'])
    media_csv_output(json_file, metadata['csv_folder'])