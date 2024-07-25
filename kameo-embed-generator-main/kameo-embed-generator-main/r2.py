import boto3
import os
from botocore.client import Config
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# CONFIG HERE
r2_access_key_id = os.getenv('R2_ACCESS_KEY_ID')
r2_secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
r2_endpoint_url = os.getenv('R2_ENDPOINT_URL')
r2_bucket_name = os.getenv('R2_BUCKET_NAME')

s3 = boto3.client('s3',
                  endpoint_url=r2_endpoint_url,
                  aws_access_key_id=r2_access_key_id,
                  aws_secret_access_key=r2_secret_access_key,
                  config=Config(signature_version='s3v4')
                  )

def upload_directory(directory_path, bucket_name, destination_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.join(destination_path, os.path.relpath(file_path, directory_path)).replace("\\", "/")
            print(f"Uploading {file_path} to {s3_key}")
            s3.upload_file(file_path, bucket_name, s3_key)
