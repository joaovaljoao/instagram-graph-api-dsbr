import os
import csv
import logging
import pickle
from PIL import Image

class ImageResizer:
    def __init__(self, csv_file):
        """Initializes the ImageResizer with the user data from a CSV file."""
        self.user_data = self.extract_user_data(csv_file)
        #print(self.user_data)

        # configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def extract_user_data(self, csv_file):
        """Extracts the user data from a CSV file and returns a list of IDs."""
        user_data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                user_data.append(row[0])

        # remove the first element (the header) and any empty elements
        user_data = user_data[1:]
        user_data = [x for x in user_data if x]

        return user_data

    def resize_image(self, image_path):
        """Resizes an image if its ID exists in the user data."""
        # extract the id from the filename
        id = os.path.splitext(image_path)[0].split('/')[-1]
        #print(id)

        # check if the id exists in the user data
        if id in self.user_data:
            # id found, resize and save the image
            with Image.open(image_path) as im:
                if im.width // 3 > 1920 or im.height // 3 > 1080:
                    im = im.resize((1920, 1080))
                elif im.width // 3 < 640 or im.height // 3 < 480:
                    im = im.resize((640, 480))
                else:
                    im = im.resize((im.width // 3, im.height // 3))
                im.save(image_path)

            # log the image resize
            self.logger.info(f'Resized image {image_path}')
        else:
            # id not found, log the image skip
            self.logger.info(f'Skipped image {image_path}')

    def process_directory(self, directory):
        """Iterates through all the JPEG files in a directory and resizes them if necessary."""
        # iterate through all the jpeg files in the directory
        for filename in os.listdir(directory):
            if not filename.endswith('.jpg'):
                continue

            # resize the image if necessary
            image_path = os.path.join(directory, filename)
            self.resize_image(image_path)

    def save(self, pickle_file):
        """Saves the ImageResizer object to a pickle file."""
        with open(pickle_file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(pickle_file):
        """Loads an ImageResizer object from a pickle file."""
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)
