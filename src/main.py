from business_data import BusinessData
from user_data import UserData
from image_downloader import InstagramImageDownloader
from image_resizer import ImageResizer

# Create the UserData instance
user_data = UserData('usernames/ifes.csv')
usernames = user_data.get_usernames()

# Specify the fields to retrieve
FIELDS = "{username,website,name,ig_id,id,profile_picture_url,\
        biography, follows_count,followers_count,media_count,\
        media{media_url,comments_count, like_count,caption,media_type,permalink,timestamp,username}}"

# Create the BusinessData instance
business_data = BusinessData()

# Create an InstagramImageDownloader instance
downloader = InstagramImageDownloader()


# Iterate over the list of usernames
for username in usernames[:2]: # Limitado a 2 para não sobrecarregar a API, Mudar na produção
    # Call the get_business_data method
    response = business_data.get_business_data(username, FIELDS)
    # Save the data to CSV files
    business_data.save_to_csv(response, username)
    downloader.download_images(response)
    resizer = ImageResizer('ifes_media.csv')
    resizer.process_directory('images')
    # save the ImageResizer object to a pickle file
    resizer.save('resizer.pkl')
