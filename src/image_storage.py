from csv_parser import read_json     
from  urllib.request import urlretrieve
from pathlib import Path


def retrieve_media_url(data, images_folder):
    for dic in data:
        if not Path(f"{images_folder}/{dic['id']}.jpg").exists():
            if dic['media_type'] != "VIDEO":
                urlretrieve(dic['media_url'], f"{images_folder}/{dic['id']}.jpg")

def retrieve_user_profile_url(dic, images_folder):
    if not Path(f"{images_folder}/{dic['business_discovery']['id']}.jpg").exists():
        urlretrieve(dic['business_discovery']['profile_picture_url'], f"{images_folder}/{dic['business_discovery']['id']}.jpg")