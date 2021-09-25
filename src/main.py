#!/usr/bin/python3
from facebook_creds import  facebook_creds
from base import metadata, csv_output, instagram_metadata_download
import warnings

warnings.filterwarnings("ignore")

path_metadata = metadata()
creds = facebook_creds()
instagram_metadata_download(path_metadata, creds)
csv_output(path_metadata)