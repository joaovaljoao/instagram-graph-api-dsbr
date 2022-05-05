import boto3
import os

class AWS_S3_Buckets:
    def __init__(self, region):
        self.region = region
        self.s3 = boto3.resource('s3', region_name=self.region)
        self.buckets = self.s3.buckets.all()
    
    #upload folder to S3
    def upload_folder(self, bucket_name, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                file_path = os.path.join(folder_path, filename)
                self.s3.Bucket(bucket_name).upload_file(file_path, filename)
                print(f"Uploaded {filename} to {bucket_name}")