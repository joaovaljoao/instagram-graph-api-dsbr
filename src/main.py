#!/usr/bin/python3
from business_data import BusinessData
from user_data import UserData
from image_downloader import InstagramImageDownloader
from image_resizer import ImageResizer
import sys
import os

# Create the UserData instance
user_data = UserData('usernames/'+sys.argv[1])
filename_prefix=sys.argv[1].split('.')[0]
usernames = user_data.get_usernames()

# Specify the fields to retrieve
FIELDS = "{username,website,name,ig_id,id,profile_picture_url,\
        biography,follows_count,followers_count,media_count,\
        media{media_url,comments_count, like_count,caption,media_type,permalink,timestamp,username}}"

# Create the BusinessData instance
business_data = BusinessData()

# Create an InstagramImageDownloader instance
downloader = InstagramImageDownloader()


# Iterate over the list of usernames
for username in usernames: # Limitado a 2 para não sobrecarregar a API, Mudar na produção
    # Call the get_business_data method
    response = business_data.get_business_data(username, FIELDS)
    # Save the data to CSV files
    if os.path.exists('pub/'+filename_prefix+'_media_data.csv') and os.path.exists('pub/'+filename_prefix+'_user_data.csv'):
        os.unlink('pub/'+filename_prefix+'_media_data.csv')
        os.unlink('pub/'+filename_prefix+'_user_data.csv')
    business_data.save_to_csv(response, filename_prefix)
    downloader.download_images(response)
    resizer = ImageResizer('pub/'+filename_prefix+'_media_data.csv')
    resizer.process_directory('pub/images')
