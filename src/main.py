#!/usr/bin/python3
from instagram_feed import InstagramGraphApi
from s3_buckets import AWS_S3_Buckets
from image_storage import retrieve_media_url
import boto3
from crud import *
import pandas as pd

if __name__ == "__main__":
    cria_dimUsers()
    cria_medias()
    
    # download instagram data
    username = pd.read_csv('input/ifes.csv', sep=';', encoding='utf-8')['username'].to_list()
    #'cnpq_oficial' #, 'cnpq_oficial', 'fapergs', 'finepinova', 'capes_oficial', 'agenciafapesp', 'fapesb'

    insta = InstagramGraphApi()
    business = insta.business_discovery(username=username[0], pages=2)

    retrieve_media_url(business, 'images')


    # s3 = boto3.client('s3')
    # s3 = AWS_S3_Buckets('us-east-1')

    # s3.upload_folder('instagram-dsbr', 'images')
