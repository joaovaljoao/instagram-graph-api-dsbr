#!/usr/bin/python3
from base import metadata, csv_output, instagram_metadata_download
import warnings

warnings.filterwarnings("ignore")

path_metadata = metadata()
instagram_metadata_download(path_metadata)
csv_output(path_metadata)
